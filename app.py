from flask import Flask, request, render_template
import json
import requests
import socket
import time
import pandas as pd
from datetime import datetime
from pymongo import MongoClient
from pymongo import errors
from src.functions import unpickle_model, update_db, run_prediction
from src.Models import Models

app = Flask(__name__)
# app._static_folder = '/Users/clayton/github/galvanize/case_studies/flask_fraud_detection/templates/'
PORT = 5353
REGISTER_URL = "http://10.3.35.189:5000/register"

client = MongoClient()
db = client.scores
raw_table = db.raw
prediction_table = db.predictions
model1 = unpickle_model('GradientBoostingClassifier.pkl')


@app.route('/hello')
def index():
	return "Hello, World!"

@app.route('/score', methods=['POST'])
def score():
    prediction = run_prediction(model1, request.json)
    update_db(request.json, prediction, raw_table)

    return ""


@app.route('/check')
def check():
    line1 = "Number of data points: {0}".format(len(DATA))
    if DATA and TIMESTAMP:
        dt = datetime.fromtimestamp(TIMESTAMP[-1])
        data_time = dt.strftime('%Y-%m-%d %H:%M:%S')
        line2 = "Latest datapoint received at: {0}".format(data_time)
        line3 = DATA[-1]
        output = "{0}\n\n{1}\n\n{2}".format(line1, line2, line3)
    else:
        output = line1
    return output, 200, {'Content-Type': 'text/css; charset=utf-8'}

@app.route('/dashboard')
def dashboard():
    return render_template('Dashboard.html')


def register_for_ping(ip, port):
    registration_data = {'ip': ip, 'port': port}
    requests.post(REGISTER_URL, data=registration_data)


if __name__ == '__main__':

    # Register for pinging service
    # # ip_address = socket.gethostbyname(socket.gethostname())
    ip_address = '10.3.35.174'
    print "attempting to register %s:%d" % (ip_address, PORT)
    register_for_ping(ip_address, str(PORT))

    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
