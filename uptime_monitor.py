import subprocess
import re
import requests

# TODO(map) Include a device name once I get all the other Pi's wired up.

# TODO(map) This command is useful for getting the data that I need about which processes
# are slowing down the Pi and maybe what I should optimize.
# -------------------------------------------------------
# ps -eo ppid,user,%cpu,%mem,comm --sort -pcpu | head -10

# TODO(map) Need to get the temperature of the Pi as well and store. This means the 
# DB will need to be updated to store that value and the endpoint will need to be updated
# to include taking in that new value as part of the JSON

# Setting up command to get user count and load averages. 
command = ['uptime']
results = subprocess.check_output(command).decode("utf-8").rstrip()
split_results = re.split(',  ', results)
load = re.split(' |, ', split_results[2])
user_count = re.split(' |, ', split_results[1])[:split_results[1].index(" user")][0]

# Setting up command to get the uptime in a user friendly output
command = ['uptime', '-p']
results = subprocess.check_output(command).decode("utf-8").rstrip()
up_time = re.split(' |, ', results[results.index(" ") + 1:])
up_time_dict = {up_time[i + 1]: up_time[i] for i in range(0, len(up_time), 2)}
up_time_minutes = 0
for key in up_time_dict.keys():
    if 'week' in key:
        up_time_minutes += int(up_time_dict[key]) * 7 * 24 * 60
    if 'day' in key:
        up_time_minutes += int(up_time_dict[key]) * 60 * 24
    if 'hour' in key:
        up_time_minutes += int(up_time_dict[key]) * 60
    if 'minute' in key:
        up_time_minutes += int(up_time_dict[key])

# Posting the data to the DB.
url = 'http://localhost:5000/uptime_stats'
headers = {'Content-Type': 'application/json'}
json_data = {'up_time': results, 'user_count': user_count, 'one_minute_load_average': load[2], 'five_minute_load_average': load[3], 'fifteen_minute_load_average': load[4], 'time': 'NOW()', 'up_time_minutes': up_time_minutes}

requests.post(url, json = json_data)
