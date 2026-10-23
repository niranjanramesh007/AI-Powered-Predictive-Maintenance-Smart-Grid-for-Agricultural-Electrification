from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('farm_data.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- AI Helper Functions ---
def predict_life(current_age, avg_lifespan, daily_hours):
    """Predicts equipment life based on usage intensity."""
    intensity_factor = 1.0
    # Refined: High usage allows up to 12 hours before heavy penalty
    if daily_hours > 12: intensity_factor = 1.5 
    elif daily_hours < 2: intensity_factor = 0.8 

    effective_age = current_age * intensity_factor
    remaining = avg_lifespan - effective_age
    return max(0, round(remaining, 1))

def predict_transformer(load_kw, capacity_kva):
    """Predicts transformer health based on load."""
    load_ratio = load_kw / capacity_kva
    if load_ratio > 0.9: return "CRITICAL OVERLOAD", "High risk of failure within 1 year"
    elif load_ratio > 0.7: return "HEAVY LOAD", "Moderate risk, reduce peak usage"
    else: return "STABLE", "Healthy operation expected"

# --- ROUTES ---

@app.route('/')
def home():
    """Landing Page"""
    return render_template('home.html')

@app.route('/about')
def about():
    """About Page"""
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Simulation Login Page"""
    if request.method == 'POST':
        # Accept any login and redirect to the calculator
        return redirect(url_for('calculator'))
    return render_template('login.html')

@app.route('/calculator')
def calculator():
    """The Main Input Form"""
    conn = get_db()
    equipments = conn.execute('SELECT * FROM equipment').fetchall()
    crops = conn.execute('SELECT * FROM crops').fetchall()
    conn.close()
    return render_template('calculator.html', equipments=equipments, crops=crops)

@app.route('/predict', methods=['POST'])
def predict():
    """The Result & Analysis Logic"""
    conn = get_db()
    eq = conn.execute('SELECT * FROM equipment WHERE id = ?', (request.form['equipment'],)).fetchone()
    crop = conn.execute('SELECT * FROM crops WHERE id = ?', (request.form['crop'],)).fetchone()
    trans = conn.execute('SELECT * FROM transformer').fetchone()
    conn.close()

    # --- 1. GET USER INPUTS ---
    age = float(request.form['age'])
    acres = float(request.form['acres'])
    actual_hours = float(request.form['hours'])
    season = request.form['season']
    # Soil input removed (assumed standard)

    # --- 2. CALCULATE AI RECOMMENDED USAGE ---
    base_water_needed = crop['water_req_liters_per_day']
    
    # Factor A: Season
    season_factor = 1.0
    if season == 'summer': season_factor = 1.4  
    elif season == 'monsoon': season_factor = 0.2 
    
    # Factor B: Efficiency (Standard ~60% loss due to evaporation/seepage)
    efficiency_factor = 0.60 

    # Factor C: Crop Specifics
    crop_name = crop['name'].lower()
    standing_water_factor = 1.0
    if 'rice' in crop_name or 'paddy' in crop_name:
        standing_water_factor = 1.5 # Rice needs standing water

    # Total Water Logic
    total_water_to_pump = (base_water_needed * acres * season_factor * standing_water_factor) / efficiency_factor
    
    # --- 3. FLOW RATE CALCULATION ---
    name_check = eq['name'].lower()
    water_keywords = ['pump', 'motor', 'sprinkler', 'valve', 'irrigation', 'compressor']
    
    if any(word in name_check for word in water_keywords):
        # Realistic Borewell Logic: 8 Liters/Hour per Watt
        estimated_flow_rate = eq['power_watts'] * 8.0 
        if estimated_flow_rate == 0: estimated_flow_rate = 2000 
        recommended_hours = total_water_to_pump / estimated_flow_rate
    else:
        # Non-pump equipment logic
        recommended_hours = actual_hours

    # Safety limits
    if recommended_hours < 0.5 and recommended_hours > 0: recommended_hours = 0.5
    recommended_hours = round(recommended_hours, 1)

    # --- 4. FINANCIAL & ENERGY CALCULATIONS ---
    # Energy Usage
    kwh_daily = (eq['power_watts'] / 1000) * actual_hours
    kwh_monthly = kwh_daily * 30
    
    # Cost Calculation (UPDATED: 446 paise = ₹4.46)
    cost_per_unit = 4.46 
    monthly_cost = round(kwh_monthly * cost_per_unit, 2)
    
    # Savings Calculation (Money saved if they follow advice)
    rec_kwh_daily = (eq['power_watts'] / 1000) * recommended_hours
    rec_monthly_cost = rec_kwh_daily * 30 * cost_per_unit
    potential_savings = round(monthly_cost - rec_monthly_cost, 2)

    # --- 5. AI PREDICTIONS ---
    life_remaining = predict_life(age, eq['lifespan_years'], actual_hours)
    trans_status, trans_msg = predict_transformer(eq['power_watts']/1000, trans['capacity_kva'])

    # --- 6. GENERATE TIP (High Sensitivity) ---
    diff = actual_hours - recommended_hours
    
    # Logic: Trigger on > 0.1 hours difference
    if diff > 0.1:
        if diff > 1.0:
            tip = f"MAJOR SAVINGS: You are running {actual_hours} hrs. AI calculates {recommended_hours} hrs is enough. Reduce immediately to save cost."
        else:
            tip = f"OPTIMIZATION: You are nearly efficient, but reducing from {actual_hours} to {recommended_hours} hrs will save small amounts of energy."
    elif diff < -0.1:
        if diff < -1.0:
            tip = f"UNDER-WATERING: {actual_hours} hrs is too low for {acres} acres. Increase to {recommended_hours} hrs to prevent crop loss."
        else:
            tip = f"SLIGHT BOOST NEEDED: Increase usage slightly to {recommended_hours} hrs for maximum yield."
    else:
        tip = "PERFECT PRECISION: Your usage is exactly what the AI recommends."

    return render_template('result.html', 
                           eq=eq, crop=crop, 
                           hours=actual_hours,
                           rec_hours=recommended_hours,
                           daily=round(kwh_daily, 2), 
                           monthly_cost=monthly_cost,    # Sent to HTML
                           savings=potential_savings,    # Sent to HTML
                           life=life_remaining,
                           trans_status=trans_status,
                           trans_msg=trans_msg,
                           tip=tip)

if __name__ == '__main__':
    app.run(debug=True)