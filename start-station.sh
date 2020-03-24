#!/bin/bash
top_scriptdir=$(dirname $BASH_SOURCE)
$scriptname=$1
$testbool=$2

echo "Starting weather station site"
node scripts/web_server.js &


echo "Running weather station..."
python app/weather_station.py -$testbool
