import pyrebase

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

data = db.child('moisture_mesurements').get()

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
            labels.append(pro_data[j]['timestemp'])
            values.append(pro_data[j]['moisture'])
            i-=1
            j+=1
    elif len(pro_data) > 30:
        i = 30
        j = len(pro_data) - 30
        while i > 0:
            labels.append(pro_data[j]['timestemp'])
            values.append(pro_data[j]['moisture'])
            i-=1
            j+=1
    return labels, values

get_labels_values(data)