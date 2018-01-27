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
mydict = {2:3, 1:89, 4:5, 3:0}

mydict = sorted(mydict.items(),key = lambda t: t[0])
print(mydict)

# rest = root.child('allComments')
# allRest = rest.get()
# for key in allRest:
#     if allRest[key]['Name'] == 'Mac':
#         theId = key
# print(theId)


# for key in allRest:
#     if rest[key]['Name'] == 'Mac':
#         answ = key
# onlineDriver.update({
# 'test': '123',
#
# })



restFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
test = restFire.get('restaurants', None)


# result = userFire.delete('forTesting','test')

# oddNum = 0
# allComments = []
# allRestr = root.child('allComments')
# allRestg = allRestr.get()
# for key in allRestg:
#     if key == 'Mac':
#         for co in allRestg[key]:
#             oddNum = oddNum + 1
#             if oddNum % 2 == 1:
#                 allComments.append(allRestg[key][co])
#
# print(allComments)
