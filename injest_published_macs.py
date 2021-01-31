import sys
import os
import csv
import requests

certified_vendors_large_path = os.path.dirname(os.path.realpath(sys.argv[0])) + '/oui.csv'
certified_vendors_medium_path = os.path.dirname(os.path.realpath(sys.argv[0])) + '/mam.csv'
certified_vendors_small_path = os.path.dirname(os.path.realpath(sys.argv[0])) + '/oui36.csv'

url = 'http://localhost:5000/vendors'
headers = {'Content-Type': 'application/json'}

with open(certified_vendors_large_path, 'r', newline='') as csvfile:
    vendor_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for vendor in vendor_reader:
        json_data = { 'reg_type': vendor[0], 'mac_address': vendor[1], 'company_name': vendor[2], 'address': vendor[3] }
        requests.post(url, json = json_data) 

with open(certified_vendors_medium_path, 'r', newline='') as csvfile:
    vendor_reader = csv.reader(csvfile, delimiter=',', quotechar='"')   
    for vendor in vendor_reader:
        json_data = { 'reg_type': vendor[0], 'mac_address': vendor[1], 'company_name': vendor[2], 'address': vendor[3] }
        requests.post(url, json = json_data) 

with open(certified_vendors_small_path, 'r', newline='') as csvfile:
    vendor_reader = csv.reader(csvfile, delimiter=',', quotechar='"')   
    for vendor in vendor_reader:
        json_data = { 'reg_type': vendor[0], 'mac_address': vendor[1], 'company_name': vendor[2], 'address': vendor[3] }
        requests.post(url, json = json_data) 
