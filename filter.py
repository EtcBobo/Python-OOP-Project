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


userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
restaurants = userFire.get('restaurants ', None)


# pricelist = []
# for key in restaurants:
#     pricelist.append(restaurants[key]['price'])
#     aprice = pricelist.sort()
#     aprice = sorted(pricelist)
#     dprice = sorted(pricelist, key=int, reverse=True)

def abc():
        userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        restaurants = userFire.get('restaurants ', None)
        alphalist = []
        for i in restaurants:
            if " " in i:
                i = i.replace(" ", "")
            #i = i.isalpha()
            alphalist.append(i)
            alphalist.sort()
            list = sorted(alphalist)
            if list == restaurants[i]['Name']:
                print(restaurants[i])


                dlist = sorted(alphalist,reverse=True)


print(list)

