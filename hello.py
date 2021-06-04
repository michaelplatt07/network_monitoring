from flask import Flask, request, jsonify
import psycopg2
import os


# TODO(map) There should be a way to interact with the endpoint such that I can approve
# a device when it pings me if I know who it is, but they haven't been on the network
# since I put this in place.
app = Flask(__name__)
db_name = os.environ['DBNAME']
db_user = os.environ['DBUSER']
db_pass = os.environ['DBPASS']
db_conn_string = "dbname=" + db_name + " user=" + db_user + " password=" + db_pass

@app.route('/')
def hello_world():
    return 'Hello, World';

@app.route('/authorized_vendors/<vendor_mac>', methods=['GET'])
def get_authorized_vendor_by_mac(vendor_mac):
    conn = psycopg2.connect(db_conn_string)
    cur = conn.cursor()
    cur.execute("SELECT * FROM certified_vendors WHERE mac_address = %s;", (vendor_mac,))
    results = cur.fetchall()
    return jsonify(results)

# TODO(map) Make more meaningful responses 
@app.route('/uptime_stats', methods=['GET', 'POST'])
def uptime_stats():
    if request.method == 'POST':
        conn = psycopg2.connect(db_conn_string)
        cur = conn.cursor()
        cur.execute("INSERT INTO uptime VALUES (%s, %s, %s, %s, %s, %s, %s);", (request.json['up_time'],request.json['user_count'],request.json['one_minute_load_average'],request.json['five_minute_load_average'],request.json['fifteen_minute_load_average'],request.json['time'],request.json['up_time_minutes']))
        conn.commit()
        cur.close()
        conn.close()
        return "Successfully posted data"
    else:
        return "TODO(map) Implement the GET method"

# TODO(map) Make more meaningful responses 
@app.route('/network_monitor_stats', methods=['GET', 'POST'])
def network_stats():
    if request.method == 'POST':
        conn = psycopg2.connect(db_conn_string)
        cur = conn.cursor()
        cur.execute("INSERT INTO network_speeds VALUES (%s, %s, %s, %s, %s);", (request.json['upload_rate'],request.json['download_rate'],request.json['time'],request.json['percent_upload_from_expected'],request.json['percent_download_from_expected']))
        conn.commit()
        cur.close()
        conn.close()
        return "Successfully posted data"
    else:
        return "TODO(map) Implement the GET method"

# TODO(map) Make more meaningful responses 
@app.route('/device_monitor_stats', methods=['GET', 'POST'])
def devices():
    if request.method == 'POST':
        conn = psycopg2.connect(db_conn_string)
        cur = conn.cursor()
        cur.execute("INSERT INTO devices VALUES (%s, %s, %s, %s, %s);", (request.json['time'],request.json['mac_address'],request.json['ip_address'],request.json['authorized'],request.json['manufacturer']))
        conn.commit()
        cur.close()
        conn.close()
        return "Successfully posted data"
    else:
        return "TODO(map) Implement the GET method"

# TODO(map) Make more meaningful responses 
@app.route('/vendors', methods=['GET', 'POST'])
def vendors():
    if request.method == 'POST':
        conn = psycopg2.connect(db_conn_string)
        cur = conn.cursor()
        cur.execute("INSERT INTO certified_vendors VALUES (%s, %s, %s, %s);", (request.json['reg_type'],request.json['mac_address'],request.json['company_name'],request.json['address']))
        conn.commit()
        cur.close()
        conn.close()
        return "Successfully posted data"
    else:
        return "TODO(map) Implement the GET method"
