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

def add_measurement(moisture, watered):
    '''
    Function to add a new measurement to db (moisture, timestamp, key = timestamp without symbols)
    It also checks if the plant got watered after measurement
        => if that is the case it enters the necessary entrys in db 
           (How much water has been used?, updating total used water for average use calculation, timestamp, updating how many liters are left in bucket)
    '''
    timestamp = str(datetime.now())[:-7]
    time = str(timestamp)[11:-3]
    data = db.child('moisture_mesurements').get()
    liters_left = db.child('liters_left').get().val()
    pump_use = db.child('pump_use').get().val()
    liter_state = liters_left['liters_left']
    key = re.sub('\.|\-|\:|\ ', '', str(datetime.now()))

    if watered == True:
        liter_state = round((liters_left['liters_left'] - pump_use['pump_use']/1000), 1)
        db.child('liters_left').set({'liters_left': liter_state})
        watered_with = pump_use['pump_use']
        db.child('watered').child('watered').child(key).set({'watered_at': timestamp, 'watered_with': watered_with})
        if db.child('watered').child('total').get().val() is None:
            total = 0
        else:
            total = db.child('watered').child('total').get().val()['total']
        total += watered_with/1000
        db.child('watered').child('total').set({'total': total})
    
    data = {'time': time, 'timestamp': timestamp, 'moisture': moisture, 'liters_left': liter_state}
    db.child('moisture_mesurements').child(key).set(data)

def get_labels_values():
    '''
    Function returns graph x and y axis from moisture_mesurements in DB
    '''
    data = db.child('moisture_mesurements').get().each()
    labels = []
    values = []
    if data is not None:
        if len(data) <= 30:
            i = len(data)
            j = 0
            while i > 0:
                labels.append(data[j].val()['time'])
                values.append(data[j].val()['moisture'])
                i-=1
                j+=1
        elif len(data) > 30:
            i = 30
            j = len(data) - 30
            while i > 0:
                labels.append(data[j].val()['time'])
                values.append(data[j].val()['moisture'])
                i-=1
                j+=1
    return labels, values

def get_average():
    '''
    Function to calculate the average use of water per week based on db entrys
    It scales per day values up to per week
    '''
    watered = db.child('watered').child('watered').get().each()
    if watered is not None:
        if len(watered) > 1:
            total = db.child('watered').child('total').get().val()['total']
            first_str = watered[0].val()['watered_at']
            last_str = watered[-1].val()['watered_at']
            first = datetime.strptime(first_str , "%Y-%m-%d %H:%M:%S")
            last = datetime.strptime(last_str , "%Y-%m-%d %H:%M:%S")
            seconds = (last - first).total_seconds()
            weeks = seconds/60/60/24/7
            average = round(total/weeks, 3)
            return str(average)+'l'
        else:
            return 'not available yet'
    else:
            return 'not available yet'

def get_last_irrigation():
    watered = db.child('watered').child('watered').get().each()
    if watered is not None:
        if len(watered) > 0:
            last_str = watered[-1].val()['watered_at']
            return last_str
        else:
            return '-'
    else:
        return '-'

@app.route('/', methods = ['GET', 'POST'])
def base_control():
    '''
    All logic for the Base Control and startup config page is implemented in this view function
    '''
    pump_use = db.child('pump_use').get().val()
    water_capacity = db.child('water_capacity').get().val()

    if request.form.get('pump_use') == "pump_use":
        if (request.form.get('pump_value')) == '':
            pass
        else:
            pump_use = int(request.form.get('pump_value'))
            db.child('pump_use').set({'pump_use': pump_use})
            if db.child('water_capacity').get().val() is not None:
                #start water loop here
                pass
    elif request.form.get('water_capacity') == "water_capacity":
        if request.form.get('water_value') == '':
            pass
        else:
            water_capacity = int(request.form.get('water_value'))
            db.child('water_capacity').set({'water_capacity': water_capacity})
            db.child('liters_left').set({'liters_left': water_capacity})
            if db.child('pump_use').get().val() is not None:
                #start water loop here
                pass
    elif request.form.get('water') == 'water':
        # watering function here
        '''
        Uncomment to add rendom measurement entry to db when pressing water button to test webapp
        add_measurement(randrange(10)/10, True)
        '''

    last_irrigation = get_last_irrigation()

    if pump_use is None or water_capacity is None:
        if db.child('pump_use').get().val() is None:
            pump_use = 'Enter new Value in '
        elif db.child('pump_use').get().val() is not None:
            pump_use = db.child('pump_use').get().val()['pump_use']
        if db.child('water_capacity').get().val() is None:
            water_capacity = 'Enter new Value in '
        elif db.child('water_capacity').get().val() is not None:
            water_capacity = db.child('water_capacity').get().val()['water_capacity']
        return render_template('start_config.html',
                                pump_use = pump_use,
                                water_capacity = water_capacity)

    labels, values = get_labels_values()
    if len(values) > 0 :
        humidity = str(int(values[-1]*100))+ '%'
    elif len(values) == 0:
        humidity = 'no measurement yet...'
    liters_left = db.child('liters_left').get().val()
    if liters_left is None:
        liter_state = 'Not available'
    else:
        if liters_left['liters_left'] <= 0:
            liter_state = 'Bucket empty'
        else: 
            liter_state = str(liters_left['liters_left'])+'l'
    average_use = get_average()
    return render_template('base_control.html',
                            labels = labels,
                            values = values,
                            humidity = humidity,
                            liter_state = liter_state,
                            average_use = average_use,
                            last_irrigation = last_irrigation)

@app.route('/advanced', methods=['POST', 'GET'])
def advanced():
    '''
    All logic for the Advanced Base Control page is implemented in this view function
    '''
    data = db.child('moisture_mesurements').get()
    pro_data = []
    if data.val() is not None:
        for i in data.each():
            pro_data.append(i.val())
    
    if request.form.get('pump_use') == "pump_use":
        if (request.form.get('pump_value')) == '':
            pass
        else:
            pump_use = int(request.form.get('pump_value'))
            db.child('pump_use').set({'pump_use': pump_use})
    elif request.form.get('water_capacity') == "water_capacity":
        if request.form.get('water_value') == '':
            pass
        else:
            water_capacity = int(request.form.get('water_value'))
            db.child('water_capacity').set({'water_capacity': water_capacity})
            db.child('liters_left').set({'liters_left': water_capacity})
    elif request.form.get('new_measure') == "new_measure":
        # manuel measurement function here
        pass
    elif request.form.get('reset') == "reset":
        db.remove()

    if db.child('pump_use').get().val() is None:
        pump_use = 'Enter new Value in '
    elif db.child('pump_use').get().val() is not None:
        pump_use = db.child('pump_use').get().val()['pump_use']

    if db.child('water_capacity').get().val() is None:
        water_capacity = 'Enter new Value in '
    elif db.child('water_capacity').get().val() is not None:
        water_capacity = db.child('water_capacity').get().val()['water_capacity']

    return render_template('advanced.html',
                            data = pro_data,
                            pump_use = pump_use,
                            water_capacity = water_capacity)


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')