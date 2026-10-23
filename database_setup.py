import sqlite3

def create_database():
    conn = sqlite3.connect('farm_data.db')
    cursor = conn.cursor()

    # --- Create Tables ---
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY,
            name TEXT,
            voltage TEXT,
            power_watts REAL,
            lifespan_years INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crops (
            id INTEGER PRIMARY KEY,
            name TEXT,
            water_req_liters_per_day REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transformer (
            id INTEGER PRIMARY KEY,
            location_id TEXT,
            installation_date TEXT,
            capacity_kva REAL
        )
    ''')

    # --- Insert Real Data ---
    
    # Equipment Data
    equipment_data = [
        (1, 'Pump 0.5 HP', '230 V', 370, 9),
        (2, 'Pump 1 HP', '230 V', 750, 10),
        (3, 'Pump 2 HP', '230 V', 1500, 11),
        (4, 'Pump 3 HP', '230 V', 2200, 12),
        (5, 'Pump 5 HP', '415 V', 3700, 13),
        (6, 'Pump 7.5 HP', '415 V', 5600, 13),
        (7, 'Pump 10 HP', '415 V', 7500, 15),
        (8, 'Sprinkler motor 1 HP', '230 V', 750, 10),
        (9, 'Sprinkler motor 3 HP', '415 V', 2200, 12),
        (10, 'Drip irrigation controller', '230 V', 370, 6),
        (11, 'Solenoid valve', '230 V', 750, 4),
        (12, 'Water level controller', '230 V', 1500, 6),
        (13, 'Soil moisture sensor', '230 V', 2200, 3),
        (14, 'Weather station sensor', '415 V', 3700, 6),
        (15, 'Electric fencing unit', '415 V', 5600, 10),
        (16, 'LED light (small)', '415 V', 7500, 10),
        (17, 'LED flood light', '230 V', 750, 12),
        (18, 'High mast LED light', '415 V', 2200, 15),
        (19, 'Control panel (idle)', '230/415 V', 20, 12),
        (20, 'Motor starter coil', '230 V', 15, 6),
        (21, 'Capacitor bank', '415 V', 200, 6),
        (22, 'CCTV camera', '12 V', 10, 6),
        (23, 'WiFi/IoT router', '230 V', 15, 4),
        (24, 'Borewell compressor', '415 V', 3000, 11),
        (25, 'Chaff cutter machine', '415 V', 2200, 12),
        (26, 'Fodder cutting machine', '415 V', 3000, 12),
        (27, 'Milking machine', '415 V', 500, 10),
        (28, 'Milk chiller', '230 V', 1500, 12),
        (29, 'Grain cleaning machine', '415 V', 4000, 13),
        (30, 'Rice mill (mini)', '415 V', 7500, 15),
        (31, 'Cold storage unit', '415 V', 5000, 17),
        (32, 'Exhaust ventilation unit', '230 V', 60, 10),
        (33, 'Polyhouse fogger motor', '230 V', 500, 6),
        (34, 'Shade net motorized roll', '230 V', 200, 10),
        (35, 'Solar inverter', '230 V', 100, 10),
        (36, 'Battery charger (solar)', '230 V', 150, 6),
        (37, 'Generator (backup)', '415 V', 5000, 12),
        (38, 'Air compressor', '415 V', 3000, 12),
        (39, 'Welding machine', '230 V', 4000, 12),
        (40, 'Water purifier (RO)', '230 V', 60, 7)
    ]
    cursor.executemany('INSERT OR REPLACE INTO equipment VALUES (?,?,?,?,?)', equipment_data)

    # Crop Data
    crop_data = [
        (1, 'Rice', 22500),
        (2, 'Wheat', 4500),
        (3, 'Maize', 5500),
        (4, 'Sugarcane', 20000),
        (5, 'Cotton', 6500),
        (6, 'Groundnut', 4500),
        (7, 'Sunflower', 4000),
        (8, 'Tomato', 6500),
        (9, 'Potato', 5500),
        (10, 'Onion', 3500),
        (11, 'Brinjal', 4500),
        (12, 'Chilli', 4000),
        (13, 'Banana', 11000),
        (14, 'Mango', 2500),
        (15, 'Coconut', 4500),
        (16, 'Tea', 5500),
        (17, 'Coffee', 3500),
        (18, 'Soyabean', 4000),
        (19, 'Cabbage', 4500),
        (20, 'Carrot', 3500)
    ]
    cursor.executemany('INSERT OR REPLACE INTO crops VALUES (?,?,?)', crop_data)

    # Transformer Data
    cursor.execute("INSERT OR REPLACE INTO transformer VALUES (1, 'Village-TR-01', '2016-01-01', 100.0)")

    conn.commit()
    conn.close()
    print("Database 'farm_data.db' created successfully!")

if __name__ == '__main__':
    create_database()