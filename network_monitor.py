import subprocess
import os
import requests
import speedtest

# TODO(map) Experiment with running subprocess.run(command, stdout=subprocess.PIPE) to see what the output looks like

s = speedtest.Speedtest()

# We are currently paying for 400 up/down
expected_speed = float(os.environ['EXPECTEDINTERNETSPEED'])

# Using the python module to get the download/upload speed
actual_download = s.download() / 1024 / 1024
actual_upload = s.upload() / 1024 / 1024

# Setting up the JSON data to post
json_data = {'upload_rate': actual_upload, 'download_rate': actual_download, 'percent_upload_from_expected': actual_upload / expected_speed, 'percent_download_from_expected': actual_download / expected_speed, 'time': 'NOW()'}

# Posting the data to the DB.
url = 'http://localhost:5000/network_monitor_stats'
headers = {'Content-Type': 'application/json'}

requests.post(url, json = json_data)
