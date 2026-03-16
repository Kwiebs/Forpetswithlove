#!/bin/bash

# Run the weather forecast script
/home/kweeb/.openclaw/workspace/weather_forecast.py

# Optional: Save to file for logging
echo "# Weather Forecast $(date)" >> /home/kweeb/.openclaw/workspace/logs/weather_forecasts.log
/home/kweeb/.openclaw/workspace/weather_forecast.py >> /home/kweeb/.openclaw/workspace/logs/weather_forecasts.log
echo "---" >> /home/kweeb/.openclaw/workspace/logs/weather_forecasts.log