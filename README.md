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
6. TODO(map) Write the remaining steps to create the tables. 

## App Environment Setup

1. Install Python3 if not already installed.
2. Create a Python virtual environment within the folder with the command `python3 -m venv ./venv`
3. Launch the virtual environment from the folder with `source venv/bin/activate`
4. Install the dependencies in the requirements.txt with `pip install requirements.txt` -- TODO(map) This step may not be the exact right command.
5. Set the following appropriate environment variables for the flask app to run
- FLASKAPP=hello.py
- FLASKENV=development
- DBNAME=networkmonitoring
- DBUSER=networkmonitor
- DBPASS=pass
- TODO(map) Include the variables required to set up texting account
<b>NOTE</b> The `FLASKENV` variable isn't stricly necessary unless you want to do development and hot reload the code.
6. Run the app with `flask run` (Including `--host=0.0.0.0` will make the app available to other computers outside of the localhost)

If the setup was done correctly the console will show the application is up and running. To test, run the command `curl localhost:5000/` and see if the response `Hello, World` comes back.

# How to Import Authorized MAC Addresses

TODO(map) Write me
