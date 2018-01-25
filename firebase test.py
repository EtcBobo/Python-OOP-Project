from flask import Flask, render_template, redirect, url_for, request, flash
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators,PasswordField,DateTimeField,SubmitField,IntegerField
from firebase import firebase
import firebase_admin
from firebase_admin import credentials, db
import random

app = Flask(__name__)
app.secret_key = 'secret123'
cred = credentials.Certificate('cred/python-oop-firebase-adminsdk-87ty7-eefcb6bc40.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://python-oop.firebaseio.com/'
})



root = db.reference()


some = input('start')

onlineDriver=root.child('forTesting')
onlineDriver.update({
'test': '123',
    'another':'345'
})

somef = input('del')
userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
result = userFire.delete('forTesting','test')

while True:
    count = input('s')
    if count == 'a':
        break
print('ok')