#!/bin/bash

# Weather Forecast Cron Setup
echo "Setting up daily weather forecast cron job..."

# Check if cron is installed
if ! command -v crontab &> /dev/null; then
    echo "Installing cron..."
    sudo apt update
    sudo apt install -y cron
    sudo systemctl enable cron
    sudo systemctl start cron
fi

# Add cron job entry
cron_entry="0 20 * * * /home/kweeb/.openclaw/workspace/run_forecast.sh"

# Check if entry already exists
if crontab -l 2>/dev/null | grep -q "/home/kweeb/.openclaw/workspace/weather_forecast.py"; then
    echo "Weather forecast cron job already exists!"
    echo "Current crontab:"
    crontab -l | grep weather
else
    # Add new job to crontab
    (crontab -l 2>/dev/null; echo "$cron_entry") | crontab -
    echo "Weather forecast cron job added!"
    echo "Next run - tomorrow at 20:00 (8:00 PM)"
fi

echo ""
echo "Current crontab entries:"
crontab -l | grep -E "(weather|forecast|marée)"

echo ""
echo "To view today's forecast manually:"
echo "python3 /home/kweeb/.openclaw/workspace/weather_forecast.py"