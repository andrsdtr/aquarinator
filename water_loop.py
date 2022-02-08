#!/usr/bin/python3 python3

import RPi.GPIO as GPIO
import datetime
from time import sleep
import pyrebase, re

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

def get_status():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(38, GPIO.IN)
    moisture = GPIO.input(38)
    #sensor outputs 0 if wet, 1 if dry, so it needs to be switched around to make sense
    if moisture == 0:
        moisture = 1
    elif moisture == 1:
        moisture = 0
    #print(moisture)
    return moisture

def pump_on():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT)
    GPIO.output(7, GPIO.LOW)
    GPIO.output(7, GPIO.HIGH)
    GPIO.output(7, GPIO.LOW)
    sleep(3)
    GPIO.output(7, GPIO.HIGH)

def water_loop():
    timestamp = str(datetime.now())[:-7]
    time = str(timestamp)[11:-3]
    data = db.child('moisture_mesurements').get()
    liters_left = db.child('liters_left').get().val()
    pump_use = db.child('pump_use').get().val()
    liter_state = liters_left['liters_left']
    key = re.sub('\.|\-|\:|\ ', '', str(datetime.now()))

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(7, GPIO.OUT) #pump
    GPIO.setup(38, GPIO.IN) #sensor

    moisture = get_status()

    if moisture == 0:
        pump_on()

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

        sleep(60*30)
        
    data = {'time': time, 'timestamp': timestamp, 'moisture': moisture, 'liters_left': liter_state}
    db.child('moisture_mesurements').child(key).set(data)

        