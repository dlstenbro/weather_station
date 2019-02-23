#!/bin/bash
top_scriptdir=$(dirname $BASH_SOURCE)

echo "Starting weather station Site"
node scripts/web_server.js &

echo "Running weather station..."
python app/weather_station.py
