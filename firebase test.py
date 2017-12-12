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

new = {'CommentNo0': {'Comment': 'First Comment'}, 'CommentNo1': {'Comment': 'second try'}, 'RatingNo0': {'Rating': '1'},
 'RatingNo1': {'Rating': '4'}, 'UserNo0': {'User': 'potato'}, 'UserNo1': {'User': 'potato'}}

restFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
#
# feedback = restFire.get(restName, None)
newFeed = []
i = 0
for key in range(int(len(new)/3)):
    newFeed.append({'user'+str(key): {'Comment': new['CommentNo'+str(key)]['Comment'], 'Rating': new['RatingNo'+str(key)]['Rating'], 'User': new['UserNo'+str(key)]['User']}})

print(newFeed)





[{'Address': '', 'Closing Hours': '12 AM', 'Comments': ''},{'Address': '', 'Closing Hours': '12 AM', 'Comments': ''}]
