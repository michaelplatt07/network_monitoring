import subprocess
import os
import requests

# TODO(map) Experiment with running subprocess.run(command, stdout=subprocess.PIPE) to see what the output looks like

# We are currently paying for 400 up/down
expected_speed = float(os.environ['EXPECTEDINTERNETSPEED'])

# Run the actual speed test
command = ['speedtest-cli']
speed_test_results = subprocess.check_output(command).decode("utf-8").split('\n')

# Setting up the JSON data to post
json_data = {'upload_rate': 0, 'download_rate': 0, 'percent_upload_from_expected': 0, 'percent_download_from_expected':0, 'time': 'NOW()'}
for result in speed_test_results:
    if "Download" in result and "Mbit" in result:
        dl_speed = float(result.split(" ")[1])
        json_data['download_rate'] = dl_speed
        json_data['percent_download_from_expected'] = dl_speed / expected_speed
    elif "Upload" in result and "Mbit" in result:
        ul_speed = float(result.split(" ")[1])
        json_data['upload_rate'] = ul_speed
        json_data['percent_upload_from_expected'] = ul_speed / expected_speed

# Posting the data to the DB.
url = 'http://localhost:5000/network_monitor_stats'
headers = {'Content-Type': 'application/json'}

requests.post(url, json = json_data)
