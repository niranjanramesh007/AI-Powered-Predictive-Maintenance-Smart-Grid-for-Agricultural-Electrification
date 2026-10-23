# Smart Farm Energy Calculator

A Flask and SQLite web application that helps explore agricultural electricity use and irrigation planning. Select a crop and piece of farm equipment, enter operating and field details, and receive estimates for irrigation runtime, electricity costs, possible savings, equipment life, and transformer loading.

> **Important:** This is an educational prototype. Its calculations and sample data are estimates, not engineering, electrical-safety, agronomic, or financial advice. Verify local crop water needs, pump flow rates, tariffs, and electrical conditions with qualified sources before making decisions.

## Contents

- [Features](#features)
- [How to use](#how-to-use)
- [How estimates are calculated](#how-estimates-are-calculated)
- [Project structure](#project-structure)
- [Requirements](#requirements)
- [Run locally](#run-locally)
- [Database](#database)
- [Routes](#routes)
- [Limitations and future improvements](#limitations-and-future-improvements)

## Features

- Home and about pages introducing the application.
- Equipment and crop selection from a local SQLite database.
- Irrigation runtime recommendations adjusted for crop, acreage, and season.
- Daily and estimated monthly electricity consumption.
- Estimated monthly electricity cost and potential cost difference if recommended hours are followed.
- Operating tips when actual hours differ from recommended hours.
- Informational equipment-life estimate based on age, rated lifespan, and usage.
- Transformer loading classification based on equipment power and the configured transformer capacity.

## How to use

1. Open the home page and choose **Start Analysis** (or open the login page).
2. Submit the login form to continue to the calculator. The current login is a demonstration only: it accepts any submitted email and password and does not authenticate or create an account.
3. Select the equipment and crop.
4. Enter the cultivated area in acres, actual equipment operating hours per day, the season, and equipment age in years.
5. Submit the form to view the analysis report, energy and cost estimates, equipment-health indicators, and recommendation.

## How estimates are calculated

The calculations are implemented in `web.py` and use the sample values in `farm_data.db`.

### Recommended irrigation runtime

The calculator begins with the crop's configured daily water requirement and multiplies it by the entered acreage. It applies a season multiplier:

| Season | Multiplier |
| --- | ---: |
| Summer | 1.4 |
| Winter / other | 1.0 |
| Monsoon | 0.2 |

Rice and paddy crops receive an additional standing-water multiplier of 1.5. The resulting amount is divided by a fixed 0.60 irrigation-efficiency factor to account for assumed water loss. For equipment whose name includes a pump, motor, sprinkler, valve, irrigation, or compressor keyword, estimated flow is rated watts multiplied by 8 liters per hour per watt; recommended hours are calculated from the estimated water amount and flow. Positive recommendations below 0.5 hours are raised to 0.5 hours, then rounded to one decimal place. For other equipment, the entered actual operating hours are used as the recommendation.

### Energy and cost

- Daily energy = equipment rated watts / 1,000 × actual operating hours.
- Monthly energy = daily energy × 30 days.
- Estimated monthly cost = monthly energy × ₹4.46 per kWh.
- Potential savings = estimated actual monthly cost minus the estimated cost at recommended hours.

The per-unit tariff is fixed in the source code and should not be treated as a current or universal electricity rate. A negative savings figure means the recommendation would increase modeled use or cost.

### Equipment life and transformer load

- Estimated remaining life is based on rated lifespan minus age adjusted by a usage factor: 1.5 for more than 12 operating hours per day, 0.8 for fewer than 2 hours, and 1.0 otherwise. The result cannot be below zero.
- Transformer loading compares the selected equipment's rated power in kW with the configured transformer capacity in kVA. A ratio above 0.9 is labeled **CRITICAL OVERLOAD**; above 0.7 is **HEAVY LOAD**; otherwise it is **STABLE**.

These are simplified indicators. They do not model motor starting current, power factor, simultaneous loads, pump curves, local weather, soil, irrigation method, or changing crop growth stages.

## Project structure

```text
.
├── web.py                  # Flask application, routes, and estimate calculations
├── database_setup.py       # Creates and fills the SQLite tables with sample data
├── farm_data.db            # SQLite database used by the application
├── requirements.txt        # Python package dependencies
├── Templates/
│   ├── home.html           # Landing page
│   ├── about.html          # Project overview
│   ├── login.html          # Demonstration login form
│   ├── calculator.html     # Equipment, crop, and farm input form
│   └── result.html         # Calculation report
└── Static/
    └── styles.css          # Shared stylesheet
```

## Requirements

- Python 3.10 or newer.
- pip.
- Flask (installed from `requirements.txt`).

## Run locally

From the project directory, create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Start the application:

```powershell
python web.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in a browser. The app uses Flask's built-in development server; do not use it as a production deployment server.

The included `farm_data.db` is ready to use. To recreate or reset its sample data, run:

```powershell
python database_setup.py
```

Run that command from the project directory. It writes `farm_data.db` in the current working directory and replaces the seeded equipment, crop, and transformer rows.

## Database

The SQLite database contains three tables:

- `equipment`: equipment name, voltage, rated power in watts, and expected lifespan in years (40 seeded entries).
- `crops`: crop name and configured daily water requirement in liters (20 seeded entries).
- `transformer`: location identifier, installation date, and capacity in kVA (one seeded transformer).

The data is illustrative and should be reviewed and localized before using the calculator for a real farm.

## Routes

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Landing page |
| GET | `/about` | Project information |
| GET, POST | `/login` | Demonstration login; POST redirects to calculator |
| GET | `/calculator` | Equipment, crop, and farm input form |
| POST | `/predict` | Generates the estimate report |

## Limitations and future improvements

- Login is not real authentication; do not enter or rely on real credentials.
- The water, efficiency, flow-rate, tariff, equipment-life, and transformer models use fixed assumptions and sample data.
- Input validation, error handling for missing or invalid database records, and automated tests can be expanded.
- Potential next steps include configurable tariffs, locally verified crop and equipment data, measured pump flow rates, user accounts, and a production-ready server configuration.
