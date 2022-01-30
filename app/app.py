from email import message
from flask import Flask, render_template
import pyrebase

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

@app.route('/')
def base_control():
    return render_template("base_control.html")

@app.route('/advanced')
def advanced():
    #db.child("names").update({"name":"andi"})
    #test = db.child("names").get()["name"]
    return render_template("advanced.html")


if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')