from flask import Flask, render_template, redirect, url_for, request, flash
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators,PasswordField,DateTimeField,SubmitField,IntegerField
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__)
app.secret_key = 'secret123'
cred = credentials.Certificate('cred/python-oop-firebase-adminsdk-87ty7-eefcb6bc40.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://python-oop.firebaseio.com/'
})


#
# restFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
# totalRes = restFire.get('restaurants', None)
# for key in totalRes:
#     print(totalRes[key])
location ='North'
filterList = [{'Address': '', 'Closing Hours': '12 AM', 'Comments': '', 'Description': 'donald', 'Food Type': 'Western Food', 'Location': 'North', 'Name': 'Mac', 'Opening Hours': '12 AM', 'Price': '10'},
              {'Address': '', 'Closing Hours': '10 PM', 'Comments': '', 'Description': 'chicken', 'Food Type': 'Chinese Food', 'Location': 'South', 'Name': 'KFC', 'Opening Hours': '8 AM', 'Price': '15'},
              {'Address': '', 'Closing Hours': '10 PM', 'Comments': '', 'Description': 'dian xin', 'Food Type': 'Chinese Food', 'Location': 'West', 'Name': 'Dim Sum', 'Opening Hours': '7 AM', 'Price': '50'},
              {'Address': '', 'Closing Hours': '12 PM', 'Comments': '', 'Description': 'yaki', 'Food Type': 'Healthy Food', 'Location': 'North', 'Name': 'Tako', 'Opening Hours': '1 AM', 'Price': '2'},
              {'Address': '', 'Closing Hours': '12 AM', 'Comments': '', 'Description': 'queen', 'Food Type': 'Western Food', 'Location': 'North', 'Name': 'Burger King', 'Opening Hours': '12 AM', 'Price': '20'},
              {'Address': 'Ang Moh Kio Mrt station', 'Closing Hours': '10 PM', 'Comments': '', 'Description': 'Japan imported', 'Food Type': 'None', 'Location': 'Central', 'Name': 'Dorayaki', 'Opening Hours': '8 AM', 'Price': '3'}]
#
# for i in range(6):
#     if location != filterList[i]['Location']:
#         del filterList[i]
#     print(i)


i = 0
while i < len(filterList):
    if filterList[i]['Location'] != location:
        del filterList[i]
        i = i -1
    i = i+1

print(filterList)






