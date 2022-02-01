from numpy import empty
from random import randrange
from flask import Flask, render_template, request
import pyrebase, re
from datetime import datetime


app = Flask(__name__)
config = {
    "apiKey": "AIzaSyCcV6PK2HiV-gw_A2YwtpQChjmjZpRzWz0",
    "authDomain": "aquarinator.firebaseapp.com",
    "databaseURL": "https://aquarinator-default-rtdb.europe-west1.firebasedatabase.app",
    "projectId": "aquarinator",
    "storageBucket": "aquarinator.appspot.com",
    "messagingSenderId": "781335927219",
    "appId": "1:781335927219:web:891a83fe25fd12027dd3c6",
    "measurementId": "G-SYW64LTQZR"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

def add_measurement(moisture): 
    timestamp = str(datetime.now())
    time = str(timestamp)[11:-10]
    liters_left = 5
    key = re.sub('\.|\-|\:|\ ', '', str(datetime.now()))
    data = {'time': time, 'timestamp': timestamp, 'moisture': moisture, 'liters_left': liters_left}
    db.child('moisture_mesurements').child(key).set(data)

def get_labels_values(data):
    labels = []
    values = []
    pro_data = []
    if data.val() is None:
        return [],[]

    for i in data.each():
        pro_data.append(i.val())
    if len(pro_data) <= 30:
        i = len(pro_data)
        j = 0
        while i > 0:
            labels.append(pro_data[j]['time'])
            values.append(pro_data[j]['moisture'])
            i-=1
            j+=1
    elif len(pro_data) > 30:
        i = 30
        j = len(pro_data) - 30
        while i > 0:
            labels.append(pro_data[j]['time'])
            values.append(pro_data[j]['moisture'])
            i-=1
            j+=1
    return labels, values

@app.route('/', methods = ['GET', 'POST'])
def base_control():
    data = db.child('moisture_mesurements').get()
    labels, values = get_labels_values(data)
    if len(values) > 0 :
        humidity = str(int(values[-1]*100))+ '%'
    elif len(values) == 0:
        humidity = 'no measurement yet...'
    
    if request.method == 'POST':
        i = 29
        # adding random values to db:

        #while i > 0: 
        #    add_measurement(randrange(10)/10)
        #    i-=1
        
        # Hier bewässerungsfunktion einfügen
    return render_template('base_control.html',
                            labels = labels,
                            values = values,
                            humidity = humidity)

@app.route('/advanced', methods=['POST', 'GET'])
def advanced():
    data = db.child('moisture_mesurements').get()
    if data.val() is not None:
        pro_data = []
        for i in data.each():
            pro_data.append(i.val())
    
    if request.form.get('pump_use') == "pump_use":
        db.child('pump_use').set({'pump_use': 1})
    elif request.form.get('water_capacity') == "water_capacity":
        db.child('water_capacity').set({'water_capacity': 1})

    if db.child('pump_use').get().val() is None:
        pump_use = 'New Value'
    elif db.child('pump_use').get().val() is not None:
        pump_use = db.child('pump_use').get().val()['pump_use']

    if db.child('water_capacity').get().val() is None:
        water_capacity = 'New Value'
    elif db.child('water_capacity').get().val() is not None:
        water_capacity = db.child('water_capacity').get().val()['water_capacity']

    return render_template('advanced.html',
                            data = pro_data,
                            pump_use = pump_use,
                            water_capacity = water_capacity)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')