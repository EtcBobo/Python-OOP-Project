import firebase_admin
from Registration import Registration
from firebase_admin import credentials, db
from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, IntegerField, validators, SelectMultipleField
from firebase import firebase
from Restaurant import Restaurant
from flask_socketio import SocketIO, emit

app = Flask(__name__)

app.config['SECRET_KEY'] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( app ) #wrap the app using the socketio

@app.route('/chat')
def hello():
  return render_template( '/chat.html' )


def messagereceived():
  print( 'message was received!!!' )

@socketio.on( 'my event' ) #To receive WebSocket messages from the client the application defines event handlers using the socketio.on decorator ,here we need to receive this event. and send it back to the server

def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) ) #call json response  and cast the json to string
  socketio.emit( 'my response', json, callback=messagereceived()) #sending a new msg from the server to this event.

#The emit() function sends a message under a custom event name.
if __name__ == '__main__':
  socketio.run( app, debug = True ) #