import subprocess
import os
import sys
import re
import time 
import requests
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# We are grabbing the MAC address of the device from the environment variable 
# because the nmap results don't show a latency and so we have to handle parsing 
# the data differently
host_mac_address = os.environ['HOSTMAC']

def configure_smtp():
    email = os.environ['EMAILSOURCE']
    password = os.environ['EMAILPASS']
    sms_gateway = os.environ['SMSGATEWAY']
    smtp = 'smtp.gmail.com'
    port = 587
    server = smtplib.SMTP(smtp, port)
    server.starttls()
    server.login(email, password)
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = sms_gateway
    msg['Subject'] = 'Unauthorized Device Detected'
    return email, sms_gateway, server, msg

def send_text(email, sms_gateway, msg, device_name, mac_address):
    body = 'Found unauthorized device ' + device_name + ' with MAC ' + mac_address
    msg.attach(MIMEText(body, 'plain'))
    sms = msg.as_string()
    server.sendmail(email, sms_gateway, sms)

def query_for_manufacturer_info(mac_dictionary, mac_address):
    url = 'http://localhost:5000/authorized_vendors/{0}'.format(''.join(mac_address.split(':')[:3]))
    response = requests.get(url).json()
    if len(response) != 0:
        mac_dictionary[mac_address]['manufacturer'] = response[0][2]
    else: 
        mac_dictionary[mac_address]['manufacturer'] = 'Not Found'

def set_authorization(mac_dictionary, mac_address):
    if mac_address in known_devices:
        mac_dictionary[mac_address]['authorized'] = True;
    else:
        mac_dictionary[mac_address]['authorized'] = False;

known_devices = []
with open(os.path.dirname(os.path.realpath(sys.argv[0])) + '/trusted_macs.txt') as trusted_macs:
    known_devices = trusted_macs.read().splitlines()

# Run the nmap scan and get back the devices
command = ['sudo', 'nmap', '-sn', '192.168.1.0/24']
nmap_results = subprocess.check_output(command).decode("utf-8").split('\n')[1:-2]

# Build a dictionary of the mac address and the IP addresses associated with them.
mac_info_dict = {}
for i in range(0, len(nmap_results), 3):
    mac_address = ''
    if 'cheekers' not in nmap_results[i] and 'MAC Address' in nmap_results[i+2]:
        result= nmap_results[i+2].split(': ')
        mac_address = result[1][:result[1].index(" ")]
        mac_info_dict[mac_address] = {}
        query_for_manufacturer_info(mac_info_dict, mac_address)
        set_authorization(mac_info_dict, mac_address)
    else:
        mac_address = host_mac_address 
        mac_info_dict[mac_address] = {}
        query_for_manufacturer_info(mac_info_dict, mac_address)
        set_authorization(mac_info_dict, mac_address)
    if 'Nmap scan report for' in nmap_results[i]:
        ip_address = nmap_results[i]
        mac_info_dict[mac_address]['ip_address'] = re.findall(r'[0-9]+(?:\.[0-9]+){3}', ip_address)[0]

# Posting the data to the DB.
url = 'http://localhost:5000/device_monitor_stats'
json_data = {'time': 'NOW()', 'mac_address': '', 'ip_address': '', 'authorized': False, 'manufacturer': ''}

for key in mac_info_dict.keys():
    json_data['mac_address'] = key
    json_data['ip_address'] = mac_info_dict[key]['ip_address']
    json_data['authorized'] = mac_info_dict[key]['authorized']
    json_data['manufacturer'] = mac_info_dict[key]['manufacturer']
    requests.post(url, json = json_data)
    if mac_info_dict[key]['authorized'] == False:
        email, sms_gateway, server, msg = configure_smtp()
        send_text(email, sms_gateway, msg, mac_info_dict[key]['manufacturer'], key)
        server.quit()
