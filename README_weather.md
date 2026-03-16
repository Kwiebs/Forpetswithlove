# Daily Weather Forecast Script Setup

## Quick Start

1. **Test the script first:**
   ```bash
   python3 /home/kweeb/.openclaw/workspace/weather_forecast.py
   ```

2. **Set up cron job automatically:**
   ```bash
   # Run the setup script (handles everything)
   ./setup_cron.sh
   ```

3. **Or set up manually:**
   ```bash
   # Add to crontab (runs at 8PM daily)
   crontab -e
   0 20 * * * /home/kweeb/.openclaw/workspace/run_forecast.sh
   ```

## What the Script Does

- Gets weather data for **Baleal** (your main location)
- Fetches tide information for **Peniche** (nearby coastal area)
- Calculates **fishing probability** based on:
  - Temperature (optimal 15-22°C)
  - Wind speed (calmer = better)
  - Precipitation (light rain OK, heavy rain bad)
  - Season factor (spring-autumn better)
- Generates formatted Portuguese weather forecast
- Saves forecasts to logs for tracking

## Features

### 🌤️ **Weather Data**
- Hourly forecasts for key times (6h, 9h, 12h, 15h, 18h)
- Temperature ranges, wind speed, precipitation probability
- UV index, clothing recommendations
- Laundry warnings with weather context

### 🌊 **Tides Information** 
- High/low tide times for Peniche
- Tide heights in meters

### 🎣 **Fishing Probability**
- Weather-based fishing score (0-100%)
- Fishing mood and tips
- Season-adjusted recommendations

## Customization

### Change Location
```python
# In weather_forecast.py, modify these coordinates:
location_baleal = {"lat": 39.3747, "lon": -9.3414}  # Your main location
location_peniche = {"lat": 39.3556, "lon": -9.3825}  # Tide location
```

### Different Cron Time
Edit crontab line:
```bash
# For 9:30 PM instead:
30 21 * * * /home/kweeb/.openclaw/workspace/run_forecast.sh

# For weekdays only:
0 20 * * 1-5 /home/kweeb/.openclaw/workspace/run_forecast.sh
```

### API Notes

**Weather Data**: Open-Meteo (free, reliable)
**Tides Data**: Uses fallback mock data due to API SSL issues in demo mode

For real tide data, you'll need:
1. **Better tides API** (WorldTides API with proper SSL certificates)
2. **API Key** (free tiers available with proper registration)
3. **Alternative tides source** (Portuguese meteorological service, etc.)

## Output Location
- **Console**: Script outputs to console when run manually
- **Log file**: `/home/kweeb/.openclaw/workspace/logs/weather_forecasts.log`

## Dependencies
- Python 3
- `requests` library: `pip install requests`

## File Structure
```
/home/kweeb/.openclaw/workspace/
├── weather_forecast.py     # Main script
├── run_forecast.sh        # Cron wrapper script  
├── logs/
│   └── weather_forecasts.log  # Log file
└── README_weather.md      # This file
```