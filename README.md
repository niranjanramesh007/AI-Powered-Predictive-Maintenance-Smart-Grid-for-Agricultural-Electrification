# Smart Farm Energy Calculator

A Flask web app that estimates agricultural equipment energy use, irrigation runtime, electricity cost, potential savings, equipment life, and transformer load.

## Run locally

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment (recommended).
3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Start the application:

   ```powershell
   python web.py
   ```

5. Open http://127.0.0.1:5000 in your browser.

The repository includes `farm_data.db`. If you need to recreate its sample data, run `python database_setup.py` from the project directory.

## Features

- Crop and equipment selection backed by SQLite data.
- Seasonal water requirement and recommended irrigation runtime estimates.
- Daily/monthly energy use, estimated cost, and potential savings.
- Informational equipment lifespan and transformer load estimates.

Calculations are estimates for demonstration and planning, not engineering guarantees. Actual water requirements, energy use, tariffs, and equipment performance vary by farm and location.
