import pyrebase, re
from datetime import datetime, timedelta
import time

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

def add_measurement(moisture, watered, timestamp):
    time = str(timestamp)[11:-3]
    data = db.child('moisture_mesurements').get()
    liters_left = db.child('liters_left').get().val()
    pump_use = db.child('pump_use').get().val()
    liter_state = liters_left['liters_left']
    key = re.sub('\.|\-|\:|\ ', '', str(timestamp) + str(datetime.now())[-7:])

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

s1 = '2022-02-09 10:33:26'
s2 = '2022-02-09 00:30:00'

FMT = '%Y-%m-%d %H:%M:%S'
tdelta = datetime.strptime(s1, FMT) + timedelta(minutes=30)
print(tdelta)

print(str(datetime.now()))
print(str(datetime.now())[-7:])

timestamp = '2022-02-08 07:03:26'

i = 60

moisture = 1

watered = False

while i > 0:
    if moisture <= 0.2:
        watered = True
    add_measurement(moisture, watered, timestamp)
    moisture -= 0.05
    moisture = round(moisture, 2)
    timestamp = str(datetime.strptime(str(timestamp), FMT) + timedelta(minutes=30))
    i -= 1
    if watered == True:
        moisture = 0.9
        watered = False