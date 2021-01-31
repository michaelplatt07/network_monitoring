# What is this app?

This app is meant to be a basic suite of network monitoring tools that can be ran locally on a computer or on a server via the Python/Flask + Postgres stack. Tools currently include:
1. Uptime -> Used to get the amount of time the computer has been running as well as the average load and user count
2. Network Monitor -> Used to measure the upload and download speed on the network
3. Device Monitor -> Used to track the devices connected to the network and flag unauthorized devices 

<b>Note</b> that this does not allow for packet sniffing (at least not yet) and it really intended at this moment to be a metric gathering application.

# Setting up the Application

To set up the application there are a few steps required to set up the Flask application:

## Postgres DB Setup

1. Install Postgres if not already installed
2. Log in as the postgres user. <b>Note</b> The next few steps work under the assumption that `networkmonitor` is the username chosen for the database but this could be something completely different if desired.
3. Create a user to be used for the database `CREATE USER networkmonitor`
4. Set the user's password with the command `ALTER USER networkmonitor WITH PASSWORD pass` where `pass` is the password to be used by the previously created user.
5. Create the database and grant access to the user that was created `CREATE DATABASE networkmonitoring WITH OWNER networkmonitor`
6. There are a few tables that need to be created within Postgres to store the data. They can be created with these commands:
- `CREATE TABLE devices (time timestamp, mac_address varchar(20), ip_address varchar(20), authorized boolean, manufacturer varchar(50));`
- `CREATE TABLE network_speeds (time timestamp, upload_rate decimal, download_rate decimal, percent_upload_from_expected decimal, percent_download_from_expected decimal);`
- `CREATE TABLE uptime(time timestamp, up_time varchar(100), user_count integer, one_minute_load_average decimal, five_minute_load_average decimal, fifteen_minute_load_average decimal, up_time_minutes bigint);`
- `CREATE TABLE certified_vendors (reg_type varchar(10), mac_address varchar(10), company_name varchar(100), address varchar(500))`

## App Environment Setup

1. Install Python3 if not already installed.
2. Create a Python virtual environment within the folder with the command `python3 -m venv ./venv`
3. Launch the virtual environment from the folder with `source venv/bin/activate`
4. Install the dependencies in the requirements.txt with `pip install -r requirements.txt`
5. Set the following appropriate environment variables for the flask app to run
- FLASKAPP=hello.py
- FLASKENV=development (This is stricly only necessary for hotswapping code during development
- DBNAME=networkmonitoring
- DBUSER=networkmonitor
- DBPASS=pass
- TODO(map) Include the variables required to set up texting account
6. Run the app with `flask run` (Including `--host=0.0.0.0` will make the app available to other computers outside of the localhost)

If the setup was done correctly the console will show the application is up and running. To test, run the command `curl localhost:5000/` and see if the response `Hello, World` comes back.

# How to Import Authorized MAC Addresses

In order to not have to pay or be limited in requests to an endpoint that looks up vendors by MAC address, this application has the ability to ingest and store public lists of MAC addresses and their vendors.

There are a series of endpoints to that end to accomplish this goal. These files are not in the repository but can be found and downloaded [here](https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries). MAC Address Block Large, Medium, and Small are the files that should be downloaded and put in this folder.

These files can then be put into the database in the `certified_vendors` table with the following command:

`python3 injest_published_macs.py`

This file looks for the `oui.csv`, `mam.csv`, and `oui36.csv` files that were downloaded from the the IEEE site previously listed. This python file can be modified to accept other files but unless the format is the same as the first three files, some additional modifications may be required.

