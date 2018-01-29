import firebase_admin
from Registration import Registration
from firebase_admin import credentials, db
from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, IntegerField, validators, SelectMultipleField, widgets
from wtforms.fields.html5 import EmailField, DateField
from firebase import firebase
from Restaurant import Restaurant
from Events import Events
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask_socketio import SocketIO, emit
import random
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from flask_share import Share
import json
import datetime


#pip install flask-socketio
# thefoodie.newsletter@gmail.com
# p/s : foodie123


cred = credentials.Certificate('cred/python-oop-firebase-adminsdk-87ty7-eefcb6bc40.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://python-oop.firebaseio.com/'
})

root = db.reference()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'jsbcfsbfjefebw237u3gdbdc'
socketio = SocketIO( app )
share = Share(app)


# GoogleMaps(app, key="AIzaSyAN-25Ihf-_ndHtyzHEXF2SGjI6U-WqQKc")

GoogleMaps(app, key="AIzaSyCrGeXVb96USi1ujzqQ7wlCwc_8LzUB-yY")



class RegisterForm(Form):
    user = StringField('Username',[validators.DataRequired()])
    password = PasswordField("Password",[validators.DataRequired()])
    passwordC = PasswordField("Confirm Password",[validators.DataRequired()])
    price = IntegerField('Preferred Price Range')
    foodType = SelectField(u'Preferred Food Type',
                           choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'), ('Western Food', 'Western Food'),
                                    ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                    ('None', 'None')])
    email = EmailField("Email")


class RestForm(Form):
    name = StringField('Restaurant Name',[validators.DataRequired()])
    desc = TextAreaField('Desciption')

    location = SelectField(u'Location', choices=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South'),('Central','Central')])


    price = IntegerField(u'Price Range (in Dollars)',[validators.DataRequired()])

    foodType = SelectField(u'Food Types',
                           choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'), ('Western Food', 'Western Food'),
                                    ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                    ('None', 'None')])
    openH = SelectField(u'Opening Hours (12am to 12am means 24 hours)',
                           choices=[('12 AM', '12 AM'),('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'), ('4 AM', '4 AM'),
                                    ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                    ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                    ('1 PM', '1 PM'),('2 PM', '2 PM'),('3 PM', '3 PM'),('4 PM', '4 PM'),('5 PM', '5 PM'),('6 PM', '6 PM'),('7 PM', '7 PM'),
                                    ('8 PM', '8 PM'),('9 PM', '9 PM'),('10 PM', '10 PM'),('11 PM', '11 PM')])
    closingH = SelectField(u'Closing Hours (12am to 12am means 24 hours)',
                           choices=[('12 AM', '12 AM'),('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'), ('4 AM', '4 AM'),
                                    ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                    ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                    ('1 PM', '1 PM'),('2 PM', '2 PM'),('3 PM', '3 PM'),('4 PM', '4 PM'),('5 PM', '5 PM'),('6 PM', '6 PM'),('7 PM', '7 PM'),
                                    ('8 PM', '8 PM'),('9 PM', '9 PM'),('10 PM', '10 PM'),('11 PM', '11 PM'),])

    address = TextAreaField('Address')

    days = SelectMultipleField('Opened Days',choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),  ('Thursday', 'Thursday'), ('Friday', 'Friday'),
                                    ('Saturday', 'Saturday'), ('Sunday','Sunday')],option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False))
class FilterForm(Form):
    fLocation = SelectField(u'Location',
                           choices=[('Any','Any'),('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South'),
                                    ('Central', 'Central')])
    pricef = SelectField(u'Price Range (Below selected price)',choices=[('05', '05'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'),
                                      ('40', '40'), ('45', '45'), ('50', '50'), ('55','55'), ('60', '60'), ('65', '65'), ('70', '70'), ('75', '75'), ('80', '80'), ('85', '85'), ('90', '95'),('100', '100')])
    openT = SelectField(u'Preferred Meal Time',
                           choices=[('12 PM', '12 PM'),('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'), ('4 AM', '4 AM'),
                                    ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                    ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 AM', '12 AM'),
                                    ('1 PM', '1 PM'),('2 PM', '2 PM'),('3 PM', '3 PM'),('4 PM', '4 PM'),('5 PM', '5 PM'),('6 PM', '6 PM'),('7 PM', '7 PM'),
                                    ('8 PM', '8 PM'),('9 PM', '9 PM'),('10 PM', '10 PM'),('11 PM', '11 PM')])
    foodType = SelectField(u'Food Types',
                           choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'), ('Western Food', 'Western Food'),
                                    ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                    ('None', 'None')])

class Feedbacks(Form):
    comments = TextAreaField('Comments')
    ratings = SelectField(u'Ratings of the restaurants (higher score means better rating)',choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])

class Sort(Form):
    sort = SelectField(u'Sort By:',
                          choices=[('Alphabetical Order', 'Alphabetical Order'), ('Lowest Price', 'Lowest Price'), ('Ratings (Higest to Lowest)', 'Ratings (Higest to Lowest)')])



class EventForm(Form):
    eventName = StringField('Event Name',[validators.DataRequired()])
    eventDescription = TextAreaField('Desciption')
    eventLocation = SelectField(u'Location', choices=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South'),('Central','Central')])
    eventAddress = TextAreaField('Place where your event is held')
    ticket = IntegerField('Entry Fee')
    startDate = StringField('Start date (e.g.2018-01-12,2018.01.12,2018/01/12)*')
    endDate = StringField('End date (e.g.2018-01-12,2018.01.12,2018/01/12)*')
    startTime = SelectField(u'Start Time(Hr)*',
                           choices=[('12 AM', '12 AM'),('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'), ('4 AM', '4 AM'),
                                    ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                    ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                    ('1 PM', '1 PM'),('2 PM', '2 PM'),('3 PM', '3 PM'),('4 PM', '4 PM'),('5 PM', '5 PM'),('6 PM', '6 PM'),('7 PM', '7 PM'),
                                    ('8 PM', '8 PM'),('9 PM', '9 PM'),('10 PM', '10 PM'),('11 PM', '11 PM')])
    endTime =  SelectField(u'End Time(Hr)*',
                           choices=[('12 AM', '12 AM'),('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'), ('4 AM', '4 AM'),
                                    ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                    ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                    ('1 PM', '1 PM'),('2 PM', '2 PM'),('3 PM', '3 PM'),('4 PM', '4 PM'),('5 PM', '5 PM'),('6 PM', '6 PM'),('7 PM', '7 PM'),
                                    ('8 PM', '8 PM'),('9 PM', '9 PM'),('10 PM', '10 PM'),('11 PM', '11 PM')])
    startTimeMin = SelectField(u'Start Time(Min)*',
                            choices= [('00', '00'), ('05', '05'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'),
                                      ('40', '40'), ('45', '45'), ('50', '50'), ('55','55')])
    endTimeMin = SelectField(u'End Time(Min)*',
                            choices= [('00', '00'), ('05', '05'), ('10', '10'), ('15', '15'), ('20', '20'), ('25', '25'), ('30', '30'), ('35', '35'),
                                      ('40', '40'), ('45', '45'), ('50', '50'), ('55','55')])

# @app.route("/location")
# def mapview():
#     map = Map(
#         identifier="map",
#         style=(
#             "height:50%;"
#             "width:100%;"
#             "top:100px;"
#             "position:absolute;"
#         ),
#         lat=1.3786539,
#         lng=103.8493234,
#         markers=[
#             {
#                 'lat':  1.372121,
#                 'lng':  103.846678,
#                 'infobox': (
#                     "<h3>Ang Mo Kio Market & Food Centre</h3>"
#                     "<p>Address: 724 Ang Mo Kio Ave 6, Singapore 560724</p>"
#                     "<p>Hours: 7AM–9PM</p>"
#                     "<p>Phone: 6225 5632</p>"
#                     "<img src='//placehold.it/50'>")
#             },
#             {
#                 'lat': 1.380936,
#                 'lng': 103.840664,
#                 'infobox': (
#                     "<h3>Ang Mo Kio 628 Market</h3>"
#                     "<p>Address: 724 Ang Mo Kio Ave 6, Singapore 560724</p>"
#                     "<p>Hours: Wednesday\t6:30AM–1:30PM</p>"
#                     "<p>Thursday\t6:30AM–1:30PM</p>"
#                     "<p>Friday\t6:30AM–1:30PM</p>"
#                     "<p>Saturday\t6:30AM–1:30PM</p>"
#                     "<p>Sunday\t6:30AM–1:30PM</p>"
#                     "<p>Monday\tClosed</p>"
#                     "<p>Tuesday\t6:30AM–1:30PM</p>"
#                     "<p>Phone: 9067 5142</p>"
#                     "<img src='//placehold.it/50'>"
#                 )
#             }
#         ]
#     )
#     return render_template('location.html', map=map)


@app.route('/', methods=['POST', 'GET'])
def home():
    try:
        userPref = session['userPref']
        proPic = session['proPic']
    except KeyError:
        userPref = {'Food Types':'None'}
        proPic =''
    print(userPref)
    recommend = []
    randRec = []
    restFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
    totalRest = restFire.get('restaurants', None)
    for key in totalRest:
        if totalRest[key]['Food Type'] == userPref['Food Types'] or userPref['Food Types'] == 'None':
            recommend.append(totalRest[key])
    option1, option2, option3 = random.sample(range(0, len(recommend)), 3)
    randRec.append(recommend[option1])
    randRec.append(recommend[option2])
    randRec.append(recommend[option3])


    list= []
    allRestr = root.child('restaurants')
    allRestg = allRestr.get()
    for key in allRestg:
        list.append(allRestg[key])

    allRat = {}
    for key in list:
        allRat[key['Name']] = float(key['Average Rating'])

    newList = [(k, allRat[k]) for k in sorted(allRat, key=allRat.get)]
    newList2 = []
    for key in newList:
        for key2 in list:
            if key[0] == key2['Name']:
                newList2.insert(0, key2)


    newList3 = []
    newList3.append(newList2[0])
    newList3.append(newList2[1])
    newList3.append(newList2[2])
    list = newList3


    nameList = []
    form = theSearch(request.form)
    if request.method == 'POST':

        name = form.name.data

        data = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")


        counter = 9999


        firebaseData = data.get('restaurants', None)

        for key in firebaseData:
            fireData = firebaseData[key]['Name']                #get restaurant names only

            fireData_low = fireData.lower()                     #lowercase

            fireData_sep = fireData_low.split()                 #split lowercase (for name that got space)

            fireData_sep_first = fireData_low.split()[0]        #get first split value

            fireData_2words = fireData_sep_first[0:2]           #get frist 2 words

            fireData_3words = fireData_sep_first[0:3]           #get first 3 words

            fireData_4words = fireData_sep_first[0:4]           #get first 4 words

            fireData_5words = fireData_sep_first[0:5]           # get first 4 words

            if fireData_low == name.lower():                    #exact match
                nameList.append(firebaseData[key])

            if name.lower() in fireData_sep:                    #split value
                nameList.append(firebaseData[key])

            if name.lower() in fireData_2words:                 #first 2 words
                nameList.append(firebaseData[key])

            elif name.lower() in fireData_3words:               #first 3 words if use if got two same results
                nameList.append(firebaseData[key])

            elif name.lower() in fireData_4words:               #first 4 words
                nameList.append(firebaseData[key])

            elif name.lower() in fireData_5words:               #first 4 words
                nameList.append(firebaseData[key])

        session['filtered'] = nameList
        return redirect(url_for('view'))
    return render_template('home.html', recommend=randRec , form=form, proPic = proPic, hnp=list)


@app.route('/chat')
def hello():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic = ''
    return render_template( '/chat.html' ,proPic=proPic)


def messagereceived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messagereceived())


class theSearch(Form):
    name = StringField('Enter the Restaurant Name')   # line you will see above search form
    plswork = StringField('try')



@app.route('/filter',methods=['POST','GET'])
def filter():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''
    filterList = []
    form = FilterForm(request.form)
    if request.method == 'POST':
        location = form.fLocation.data
        pricef = form.pricef.data
        foodType = form.foodType.data
        openT = form.openT.data


        restFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        totalRest = restFire.get('restaurants',None)



        for key in totalRest:
            if totalRest[key]['Opening Hours'] == '12 PM':
                openH = 12
            elif totalRest[key]['Opening Hours'] == '12 AM':
                openH = 0
            elif totalRest[key]['Opening Hours'][-2:] == 'PM':
                openH = int(totalRest[key]['Opening Hours'][0:2]) + 12
            else:
                openH = int(totalRest[key]['Opening Hours'][0:2])

            if totalRest[key]['Closing Hours'] == '12 PM':
                closingH = 12
            elif totalRest[key]['Closing Hours'] == '12 AM':
                closingH = 0
            elif totalRest[key]['Closing Hours'][-2:] == 'PM':
                closingH = int(totalRest[key]['Closing Hours'][0:2]) + 12
            else:
                closingH = int(totalRest[key]['Closing Hours'][0:2])

            if openT == '12 PM':
                openT1 = 12
            elif openT == '12 AM':
                openT1 = 0
            elif openT[-2:] == 'PM':
                openT1 = int(openT[0:2]) +12
            else:
                openT1 = int(openT[0:2])

            if openH <= openT1 < closingH or openT1 < closingH < openH or openT1 > openH > closingH or closingH == openH:
                filterList.append(totalRest[key])

            if location !='Any':
                i = 0
                while i < len(filterList):
                    if filterList[i]['Location'] != location:
                        del filterList[i]
                        i = i - 1
                    i = i + 1



        if pricef != '':
            i = 0
            while i < len(filterList):
                if int(filterList[i]['Price']) > int(pricef):
                    del filterList[i]
                    i = i - 1
                i = i + 1

            print(filterList)

        if foodType != 'None':
            i = 0
            while i < len(filterList):
                if filterList[i]['Food Type'] != foodType:
                    del filterList[i]
                    i = i - 1
                i = i + 1


        session['filtered'] = filterList
        print(session['filtered'])
        return redirect(url_for('view'))
    return render_template('filter.html', form=form,proPic=proPic)


@app.route('/uploadtest',methods=['POST','GET'])
def uploadtest():
    return render_template('uploadtest.html')


@app.route('/data')
def data():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''
    list =[]
    # data = firebase.FirebaseApplication("https://jsmap-a2929.firebaseio.com/")
    # firebaseData = data.get('location', None)

    data = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
    firebaseData = data.get('locations', None)

    list.append(firebaseData)

    # for key in firebaseData:
    #     data = firebaseData[key]
    #     list.append(data)

    json_string = json.dumps(list)



    return render_template('data.html' , s_data = json_string, proPic = 'proPic')


@app.route('/viewallRest',methods=['POST','GET'])
def viewall():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''
    list= []
    allRestr = root.child('restaurants')
    allRestg = allRestr.get()
    for key in allRestg:
        list.append(allRestg[key])
    print(list)
    listLen = len(list)


    form = Sort(request.form)
    if request.method == 'POST':
        sort = form.sort.data
        if sort == 'Alphabetical Order':
            allAlpha =[]
            for key in list:
                allAlpha.append(key['Name'])
            allAlpha = sorted(allAlpha)
            newList = []
            for i in range(len(list)):
                for key in list:
                    if key['Name'] == allAlpha[i]:
                        newList.append(key)
            list = newList

        elif sort == 'Lowest Price':
            allPrice = {}
            for key in list:
                allPrice[key['Name']] = int(key['Price'])

            newList = [(k, allPrice[k]) for k in sorted(allPrice, key=allPrice.get)]
            newList2 = []
            for key in newList:
                for key2 in list:
                    if key[0] == key2['Name']:
                        newList2.append(key2)
            list = newList2
        elif sort == 'Ratings (Higest to Lowest)':
            allRat = {}
            for key in list:
                allRat[key['Name']] = int(key['Average Rating'])

            newList = [(k, allRat[k]) for k in sorted(allRat, key=allRat.get)]
            newList2 = []
            for key in newList:
                for key2 in list:
                    if key[0] == key2['Name']:
                        newList2.insert(0,key2)
            list = newList2

        return render_template('viewallRest.html', Restaurant=list, lengthList=listLen, proPic=proPic, form=form)
    return render_template('viewallRest.html', Restaurant=list, lengthList = listLen,proPic=proPic,form=form)

@app.route('/viewRest',methods=['POST','GET'])
def view():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''
    list = session['filtered']
    listLen = len(list)


    form = Sort(request.form)
    if request.method == 'POST':
        sort = form.sort.data
        if sort == 'Alphabetical Order':
            allAlpha =[]
            for key in list:
                allAlpha.append(key['Name'])
            allAlpha = sorted(allAlpha)
            newList = []
            for i in range(len(list)):
                for key in list:
                    if key['Name'] == allAlpha[i]:
                        newList.append(key)
            list = newList

        elif sort == 'Lowest Price':
            allPrice = {}
            for key in list:
                allPrice[key['Name']] = int(key['Price'])

            newList = [(k, allPrice[k]) for k in sorted(allPrice, key=allPrice.get)]
            newList2 = []
            for key in newList:
                for key2 in list:
                    if key[0] == key2['Name']:
                        newList2.append(key2)
            list = newList2
        elif sort == 'Ratings (Higest to Lowest)':
            allRat = {}
            for key in list:
                allRat[key['Name']] = float(key['Average Rating'])

            newList = [(k, allRat[k]) for k in sorted(allRat, key=allRat.get)]
            newList2 = []
            for key in newList:
                for key2 in list:
                    if key[0] == key2['Name']:
                        newList2.insert(0,key2)
            list = newList2

        return render_template('viewRest.html', Restaurant=list, lengthList=listLen, proPic=proPic, form=form)
    return render_template('viewRest.html', Restaurant=list, lengthList = listLen,proPic=proPic,form=form)


@app.route('/addRest',methods=['POST','GET'])
def addRest():

    try:
        proPic = session['proPic']
        user = session['username']
    except KeyError:
        proPic =''
        user = ''
    form = RestForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        desc = form.desc.data
        location = form.location.data
        price = form.price.data
        foodType = form.foodType.data
        openH = form.openH.data
        closingH = form.closingH.data
        address = form.address.data
        days = form.days.data

        if days == []:
            days = {'0':'Everyday'}
            print('this')

        res = Restaurant(name,desc,location,price,foodType,openH,closingH,address)

        restFirer = root.child('restaurants')
        try:
            for key in restFirer:
                if name == key:
                    flash('This restaurant already exist')
                    return redirect(url_for('addRest'))
        except:
            pass
        if user == '':
            flash('You must be logged in to recommend a Restaurant')
            return redirect(url_for('addRest'))
        restFireu = root.child('restaurants/'+name)
        restFireu.update({
            'Name':res.get_name(),
            'Description': res.get_description(),
            'Location': res.get_location(),
            'Price': res.get_price(),
            'Food Type': res.get_foodType(),
            'Opening Hours': res.get_openH(),
            'Closing Hours': res.get_closingH(),
            'Address': res.get_address(),
            'User':session['username'],
            'Average Rating':0,
            'Number of Raters':0,
            'Days':days
        })
        flash('You have added a new Restaurant!')
        # theBreak = False
        # while theBreak != True:
        #     allPicr = root.child('restPic')
        #     allPicg = allPicr.get()
        #     for key in allPicg:
        #         if allPicg[key]['rest'] == 'placeholder':
        #             rightUser = root.child('restPic/' + key)
        #             rightUser.update({
        #                 'rest': res.get_name()
        #             })
        #             theBreak = True
        return redirect(url_for('home'))
    return render_template('addRest.html', form=form,proPic=proPic,user=user)


@app.route('/userRegister',methods=['POST','GET'])
def userRegister():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''

    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.user.data
        password = form.password.data
        price = form.price.data
        foodType = form.foodType.data
        email = form.email.data

        passwordC = form.passwordC.data
        if password != passwordC:
            flash('The passwords does not match')
            return redirect(url_for('userRegister'))


        reg = Registration(user,password,price,foodType,email)

        userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        allUser = userFire.get('allUsers',None)
        for key in allUser:
            if allUser[key]['Username'] == user:
                flash('This username has already been used')
                return redirect(url_for('userRegister'))
            if allUser[key]['Email'] == email and email != '':
                flash('This email has already been used')
                return redirect(url_for('userRegister'))

        if email != '':

            email_user = 'thefoodie.newsletter@gmail.com'
            email_password = 'foodie123'
            email_send = email

            subject = 'Warm welcome from TheFoodie team!'

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subject

            body = '\n Hi '  + user + '! Thank you for subscribing with TheFoodie Newsletter! \n As a welcome gift, get a free sundae and mcwings by using the codes given below ' \
                   '\n \nPlease continue to look forward to our monthly newsletters and get exclusive promotion codes only for subscribers! ' \
                   '\n \n \n Sincerely, ' \
                   '\n \nTheFoodie Team'

            msg.attach(MIMEText(body, 'plain'))

            filename = 'promo.jpg'
            attachment = open(filename, 'rb')

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + filename)

            msg.attach(part)
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_send, text)
            server.quit()

        try:
            totalUsers = userFire.get('allUsers',None)
            count = len(totalUsers)
        except TypeError:
            count = 0
        userFire.put('allUsers','user'+str(count),{
            'Username': reg.get_user(),
            'Password': reg.get_password(),
            'Price': reg.get_price(),
            'Food Types': reg.get_foodType(),
            'Email':reg.get_email()
        })
        flash('You have succesfully registered!')
        theBreak = False
        while theBreak != True:
            allPic = userFire.get('userPic', None)
            for key in allPic:
                if allPic[key]['user'] == 'placeholder':
                    rightUser = root.child('userPic/'+key)
                    rightUser.update({
                        'user': reg.get_user()
                    })
                    theBreak = True
        return redirect(url_for('home'))
    return render_template('userRegister.html', form=form,proPic=proPic)


@app.route('/userLogin',methods=['POST','GET'])
def userLogin():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''
    logCheck = False
    form = RegisterForm(request.form)
    if request.method == 'POST':
        user = form.user.data
        password = form.password.data
        userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        totalUsers = userFire.get('allUsers',None)
        allPic = userFire.get('userPic',None)
        for key in totalUsers:
            if password == totalUsers[key]['Password'] and user == totalUsers[key]['Username']:
                session['logged_in'] = True
                session['username'] = totalUsers[key]['Username']
                flash('You are successfully logged in')
                session['userPref'] = totalUsers[key]
                session['userDetail'] = totalUsers[key]
                for key2 in allPic:
                    if user == allPic[key2]['user']:
                        session['proPic'] = allPic[key2]['urlProfile']
                print(totalUsers[key])
                logCheck = True
                return redirect(url_for('home'))
        if logCheck == False:
            flash('Invalid Username or Password')
            session['logged_in'] = False

    return render_template('userLogin.html', form=form,proPic=proPic)

@app.route('/heatmap')
def heatmap():
    centralmap1 = Map(
        identifier="D10map",
        lat=1.3343035,
        lng=103.85632650000002,
        markers=[
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': 1.324914617739032,
                'lng': 103.85094881057739,
                'infobox': "<b>360 Balestier Rd, Singapore"
            },
            {
                'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                'lat': 1.3209138285600572,
                'lng': 103.89117121696472,
                'infobox': "<b>70a Paya Lebar Rd, Singapore</b>"
            }

        ]
    )


    return render_template('heatmap.html', Centralmap1= centralmap1)

@app.route('/restDet/<restName>',methods=['POST','GET'])
def restPage(restName):
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''
    restName = restName
    form = Feedbacks(request.form)

    allRestr = root.child('restaurants/'+restName)
    print('all',allRestr.get())
    restDetail = allRestr.get()


    """load all comments and ratings, and put all comments into a list"""
    try:
        counter = 0
        allComments = []
        allUsers = []
        allCommr = root.child('allComments')
        allPicr = root.child('userPic')
        allPicg = allPicr.get()
        allCommg = allCommr.get()
        for key in allCommg:
            if key == restName:
                for i in allCommg[key]:
                    if counter < int(len(allCommg[key])/2):
                        allComments.insert(0,allCommg[key][i])
                    else:
                        allUsers.insert(0,allCommg[key][i])
                    counter = counter +1

        allPic = []
        for i in range(len(allUsers)):
            for key in allPicg:
                if allUsers[i] == allPicg[key]['user']:
                   allPic.append(allPicg[key]['urlProfile'])


        allRatings =[]
        allRatr = root.child('allRatings')
        allRatg = allRatr.get()
        for key in allRatg:
            if key == restName:
                for co in allRatg[key]:
                    allRatings.insert(0,int(allRatg[key][co]))
    except:
        allComments = []
        allUsers = []
        allRatings = []
        allPic = []



    if request.method == 'POST':
        try:
            comments = form.comments.data
            ratings = form.ratings.data
            try:
                pushCommr = root.child('allComments/'+restName)
                pushCommg = pushCommr.get()
                theIndex = int(len(pushCommg)/2)
            except:
                pushCommr = root.child('allComments/'+restName)
                theIndex = 0
            pushCommr.update({
                'comment'+str(theIndex):comments,
                'user'+str(theIndex):session['username']
            })
            pushRatr = root.child('allRatings/'+restName)
            pushRatr.update({
                'rating'+str(theIndex):ratings
            })

            allRestr = root.child('restaurants/' + restName)
            print('all', allRestr.get())


            currRatg = pushRatr.get()
            totalRating = 0

            for key in currRatg:
                totalRating = totalRating + int(currRatg[key])
            numRaters = len(currRatg)
            avgRatings = round(totalRating/numRaters,1)
            allRestr.update({
                'Average Rating':avgRatings,
                'Number of Raters':numRaters
            })
            print(avgRatings,numRaters)
            restDetail = allRestr.get()



            try:
                counter = 0
                allComments = []
                allUsers = []
                allCommr = root.child('allComments')
                allCommg = allCommr.get()
                for key in allCommg:
                    if key == restName:
                        for i in allCommg[key]:
                            if counter < int(len(allCommg[key]) / 2):
                                allComments.insert(0,allCommg[key][i])
                            else:
                                allUsers.insert(0,allCommg[key][i])
                            counter = counter + 1

                allPic = []
                for i in range(len(allUsers)):
                    for key in allPicg:
                        if allUsers[i] == allPicg[key]['user']:
                            allPic.append(allPicg[key]['urlProfile'])

                allRatings = []
                allRatr = root.child('allRatings')
                allRatg = allRatr.get()
                for key in allRatg:
                    if key == restName:
                        for co in allRatg[key]:
                            allRatings.insert(0,int(allRatg[key][co]))
            except:
                allComments = []
                allUsers = []
                allRatings = []
                allPic = []



            return render_template('restDet.html', restDetail=restDetail, form=form, comments=allComments, users=allUsers,
                                   ratings=allRatings, proPic=proPic, pic=allPic)
        except:
            flash('You must login to be able to comment or rate restaurants')
            return render_template('restDet.html',restDetail = restDetail, form=form,comments=allComments,users=allUsers,ratings=allRatings,proPic=proPic, pic=allPic)

    return render_template('restDet.html',restDetail = restDetail, form=form,comments=allComments,users=allUsers,ratings=allRatings,proPic=proPic, pic=allPic)



@app.route('/eventEdit/<eventName>',methods=['POST','GET'])
def eventEdit(eventName):
    try:
        proPic = session['proPic']
    except KeyError:
        session['proPic'] = ''

    eventName = eventName
    theEventr = root.child('events/'+eventName)
    theEventg = theEventr.get()

    class EventForm2(Form):
        eventDescription = TextAreaField('Desciption',default=theEventg['Description'])
        eventLocation = SelectField(u'Location',
                                    choices=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South'),
                                             ('Central', 'Central')],default=theEventg['Location'])
        eventAddress = TextAreaField('Place where your event is held',default=theEventg['Address'])
        ticket = IntegerField('Entry Fee',default=theEventg['ticket'])
        startDate = StringField('Start date (e.g.2018-01-12)*',default=theEventg['Start'])
        endDate = StringField('End date (e.g.2018-01-12)*',default=theEventg['End'])
        startTime = SelectField(u'Start Time(Hr)*',
                                choices=[('12 AM', '12 AM'), ('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'),
                                         ('4 AM', '4 AM'),
                                         ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                         ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                         ('1 PM', '1 PM'), ('2 PM', '2 PM'), ('3 PM', '3 PM'), ('4 PM', '4 PM'),
                                         ('5 PM', '5 PM'), ('6 PM', '6 PM'), ('7 PM', '7 PM'),
                                         ('8 PM', '8 PM'), ('9 PM', '9 PM'), ('10 PM', '10 PM'), ('11 PM', '11 PM')],default=theEventg['Time Start'])
        endTime = SelectField(u'End Time(Hr)*',
                              choices=[('12 AM', '12 AM'), ('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'),
                                       ('4 AM', '4 AM'),
                                       ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                       ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                       ('1 PM', '1 PM'), ('2 PM', '2 PM'), ('3 PM', '3 PM'), ('4 PM', '4 PM'),
                                       ('5 PM', '5 PM'), ('6 PM', '6 PM'), ('7 PM', '7 PM'),
                                       ('8 PM', '8 PM'), ('9 PM', '9 PM'), ('10 PM', '10 PM'), ('11 PM', '11 PM')],default=theEventg['Time End'])
        startTimeMin = SelectField(u'Start Time(Min)*',
                                   choices=[('00', '00'), ('05', '05'), ('10', '10'), ('15', '15'), ('20', '20'),
                                            ('25', '25'), ('30', '30'), ('35', '35'),
                                            ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55')],default=theEventg['Min Start'])
        endTimeMin = SelectField(u'End Time(Min)*',
                                 choices=[('00', '00'), ('05', '05'), ('10', '10'), ('15', '15'), ('20', '20'),
                                          ('25', '25'), ('30', '30'), ('35', '35'),
                                          ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55')],default=theEventg['Min End'])

    form = EventForm2(request.form)
    if request.method == 'POST':
        eventDescription = form.eventDescription.data
        eventLocation = form.eventLocation.data
        eventAddress = form.eventAddress.data
        startDate = form.startDate.data
        endDate = form.endDate.data
        startTime = form.startTime.data
        endTime = form.endTime.data
        startTimeMin = form.startTimeMin.data
        endTimeMin = form.endTimeMin.data
        ticket = form.ticket.data

        try:
            user = session['username']
        except:
            flash('You must be logged in to add an Event')
            return render_template('eventEdit.html', form=form, proPic=session['proPic'])

        try:
            theCheck = True
            if int(startDate[0:4]) == int(endDate[0:4]):
                if int(startDate[5:7]) == int(endDate[5:7]):
                    if int(startDate[8:]) > int(endDate[8:]):
                        theCheck = False
                elif int(startDate[5:7]) > int(endDate[5:7]):
                    theCheck = False
            elif int(startDate[0:4]) > int(endDate[0:4]):
                theCheck = False

            if theCheck == False:
                flash('The End Date cannot be before the Start Date')
                return render_template('eventEdit.html', form=form, proPic=session['proPic'], eventName=eventName)
        except:
            flash('Please follow the example date format')
            return render_template('eventEdit.html', form=form, proPic=session['proPic'], eventName=eventName)

        if ticket == '':
            ticket = 0

        theEventr.update({
            'Description': eventDescription,
            'Location': eventLocation,
            'Address': eventAddress,
            'Start': startDate,
            'End': endDate,
            'Time Start': startTime,
            'Time End': endTime,
            'Min Start': startTimeMin,
            'Min End': endTimeMin,
            'ticket': ticket
        })
        flash('You have successfully edited your Event!')
        return redirect(url_for('home'))

    return render_template('eventEdit.html', form=form, proPic=session['proPic'],eventName=eventName)


@app.route('/restEdit/<restName>',methods=['POST','GET'])
def restEdit(restName):
    try:
        proPic = session['proPic']
    except KeyError:
        session['proPic'] = ''
    restName = restName
    theRestr = root.child('restaurants/'+restName)
    theRestg = theRestr.get()

    class RestForm2(Form):
        desc = TextAreaField('Desciption', default=theRestg['Description'])

        location = SelectField(u'Location',
                               choices=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South'),
                                        ('Central', 'Central')],default=theRestg['Location'])

        price = SelectField(u'Price Range',
                            choices=[(80, 80), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'),
                                     ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'),
                                     ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16')],default=theRestg['Price'])
        foodType = SelectField(u'Food Types',
                               choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'),
                                        ('Western Food', 'Western Food'),
                                        ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                        ('None', 'None')],default=theRestg['Food Type'])
        openH = SelectField(u'Opening Hours',
                            choices=[('12 AM', '12 AM'), ('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'),
                                     ('4 AM', '4 AM'),
                                     ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                     ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                     ('1 PM', '1 PM'), ('2 PM', '2 PM'), ('3 PM', '3 PM'), ('4 PM', '4 PM'),
                                     ('5 PM', '5 PM'), ('6 PM', '6 PM'), ('7 PM', '7 PM'),
                                     ('8 PM', '8 PM'), ('9 PM', '9 PM'), ('10 PM', '10 PM'), ('11 PM', '11 PM')],default=theRestg['Opening Hours'])
        closingH = SelectField(u'Closing Hours',
                               choices=[('12 AM', '12 AM'), ('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'),
                                        ('4 AM', '4 AM'),
                                        ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                        ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                        ('1 PM', '1 PM'), ('2 PM', '2 PM'), ('3 PM', '3 PM'), ('4 PM', '4 PM'),
                                        ('5 PM', '5 PM'), ('6 PM', '6 PM'), ('7 PM', '7 PM'),
                                        ('8 PM', '8 PM'), ('9 PM', '9 PM'), ('10 PM', '10 PM'), ('11 PM', '11 PM'), ],default=theRestg['Closing Hours'])

        address = TextAreaField('Address',default=theRestg['Address'])

    form = RestForm2(request.form)
    if request.method == 'POST':

        desc = form.desc.data
        location = form.location.data
        price = form.price.data
        foodType = form.foodType.data
        openH = form.openH.data
        closingH = form.closingH.data
        address = form.address.data

        theRestr.update({
            'Description': desc,
            'Location': location,
            'Price': price,
            'Food Type': foodType,
            'Opening Hours': openH,
            'Closing Hours': closingH,
            'Address': address
        })
        flash('You have successfully edited your restaurant!')
        return redirect(url_for('home'))
    return render_template('restEdit.html', form=form, proPic=session['proPic'],rest = theRestg)

@app.route('/userEdit',methods=['POST','GET'])
def userEdit():
    try:
        proPic = session['proPic']
    except KeyError:
        session['proPic'] =''
    class UserEdit(Form):
        password = PasswordField("Password", [validators.DataRequired()])
        passwordC = PasswordField("Confirm Password", [validators.DataRequired()])
        price = StringField('Preferred Price Range',default=session['userDetail']['Price'])
        foodType = SelectField(u'Preferred Food Type',
                               choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'),
                                        ('Western Food', 'Western Food'),
                                        ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                        ('None', 'None')], default=session['userDetail']['Food Types'])
        email = EmailField("Email", [validators.optional()], default=session['userDetail']['Email'])
    form = UserEdit(request.form)
    userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
    allUser = userFire.get('allUsers', None)
    allPic = userFire.get('userPic', None)
    count = 0
    for key in allPic:
        if session['username'] == allPic[key]['user']:
            count = int(allPic[key]['counter']) +1


    if request.method == 'POST' and form.validate():
        email = form.email.data
        price = form.price.data
        foodType = form.foodType.data
        password = form.password.data
        passwordC = form.passwordC.data
        if password != passwordC:
            flash('The passwords does not match')
            return redirect(url_for('userEdit'))

        for key in allUser:
            if session['username'] == allUser[key]['Username']:
                thekey = key


        userFire.put('allUsers', thekey, {
            'Username': session['username'],
            'Price': price,
            'Food Types': foodType,
            'Email': email,
            'Password': password
        })
        flash('You have succesfully edited your profile!')
        for key in allUser:
            if session['username'] == allUser[key]['Username']:
                session['userDetail'] = allUser[key]

        theBreak = False
        while theBreak == False:
            userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
            allPic = userFire.get('userPic', None)
            for key in allPic:
                if session['username'] == allPic[key]['user'] and int(allPic[key]['counter']) == count-1:
                    toDelete = key
                    theBreak = True
        result = userFire.delete('userPic', toDelete)

        for key in allPic:
            if session['username'] == allPic[key]['user']:
                session['proPic'] = allPic[key]['urlProfile']
        print(session['userDetail'])
        return redirect(url_for('home'))
    return render_template('userEdit.html', form=form, user=session['userDetail'], proPic=session['proPic'], count=str(count))


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('userLogin'))

@app.route('/userProfile')
def userProfile():
    try:
        proPic = session['proPic']
    except KeyError:
        session['proPic'] =''
    userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
    totalUsers = userFire.get('allUsers', None)
    for key in totalUsers:
        if totalUsers[key]['Username'] == session['username']:
            theUser = totalUsers[key]
    print(theUser)
    allRestr = root.child('restaurants')
    allRestg = allRestr.get()
    allEdit = []
    for key in allRestg:
        if allRestg[key]['User'] == theUser['Username']:
            allEdit.append(allRestg[key])

    allEventr = root.child('events')
    allEventg =allEventr.get()
    allEvent = []
    for key in allEventg:
        if allEventg[key]['User'] == theUser['Username']:
            allEvent.append(allEventg[key])

    goingEvent = []
    for key in allEventg:
        try:
            for key2 in allEventg[key]['Going']:
                if allEventg[key]['Going']['Name'] == theUser['Username']:
                    goingEvent.append(allEventg[key])
        except:
            pass

    return render_template('userProfile.html' , user = theUser, proPic = session['proPic'],allEdit=allEdit,allEvent=allEvent,goingEvent=goingEvent)


@app.route('/events', methods=['POST','GET'])
def events():
    try:
        proPic = session['proPic']
    except KeyError:
        session['proPic'] =''

    allEventr = root.child('events')
    allEventg = allEventr.get()

    now = datetime.datetime.now()
    currYear = now.year
    currMonth = now.month
    currDate = now.day

    status = []
    count = 0

    for key in allEventg:
        if int(allEventg[key]['Start'][0:4]) > currYear:
            status.append('Upcoming')
        elif int(allEventg[key]['Start'][0:4]) < currYear:
            status.append('Ended')
        elif int(allEventg[key]['Start'][0:4]) == currYear:
            if int(allEventg[key]['Start'][5:7]) > currMonth:
                status.append('Upcoming')
            elif int(allEventg[key]['Start'][5:7]) < currMonth:
                status.append('Ended')
            elif int(allEventg[key]['Start'][5:7]) == currMonth:
                if int(allEventg[key]['Start'][8:]) > currDate:
                    status.append('Upcoming')
                elif int(allEventg[key]['Start'][8:]) < currDate:
                    status.append('Ended')
                elif int(allEventg[key]['Start'][8:]) == currDate:
                    status.append('Ongoing')

    for key in allEventg:
        eventr = root.child('events/'+key)
        eventr.update({
            'Status':status[count]
        })
        count = count +1

    for key in allEventg:
        count2 = 0
        try:
            for key2 in allEventg[key]['Going']:
                count2 = count2 + 1
        except:
            count2 = 0
        peopler = root.child('events/'+key)
        peopler.update({
            'People':count2
        })



    theList = []
    ongoing = []
    upcoming = []
    ended = []
    allEventr = root.child('events')
    allEventg = allEventr.get()

    for key in allEventg:
        theList.append(allEventg[key])

    for key in allEventg:
        if allEventg[key]['Status'] == 'Ongoing':
            ongoing.append(allEventg[key])

    for key in allEventg:
        if allEventg[key]['Status'] == 'Upcoming':
            upcoming.append(allEventg[key])

    for key in allEventg:
        if allEventg[key]['Status'] == 'Ended':
            ended.append(allEventg[key])



    allPop = {}
    for key in theList:
        if key['Status'] == 'Ongoing' or key['Status'] == 'Upcoming':
            allPop[key['Name']] = key['People']

    newList = [(k, allPop[k]) for k in sorted(allPop, key=allPop.get)]
    newList2 = []
    for key in newList:
        for key2 in theList:
            if key[0] == key2['Name']:
                newList2.insert(0, key2)
    popEvent = newList2



    form = EventForm(request.form)
    if request.method =='POST' and form.validate():
        eventName = form.eventName.data
        eventDescription = form.eventDescription.data
        eventLocation = form.eventLocation.data
        eventAddress = form.eventAddress.data
        startDate = form.startDate.data
        endDate = form.endDate.data
        startTime = form.startTime.data
        endTime = form.endTime.data
        startTimeMin = form.startTimeMin.data
        endTimeMin = form.endTimeMin.data
        ticket = form.ticket.data

        try:
            user = session['username']
        except:
            flash('You must be logged in to add an Event')
            return redirect(url_for('events'))

        try:
            theCheck = True
            if int(startDate[0:4]) == int(endDate[0:4]):
                if int(startDate[5:7]) == int(endDate[5:7]):
                    if int(startDate[8:]) > int(endDate[8:]):
                        theCheck = False
                elif int(startDate[5:7]) > int(endDate[5:7]):
                    theCheck = False
            elif int(startDate[0:4]) > int(endDate[0:4]):
                theCheck = False

            if theCheck == False:
                flash('The End Date cannot be before the Start Date')
                return redirect(url_for('events'))
        except:
            flash('Please follow the example date format')
            return redirect(url_for('events'))

        if ticket == '':
            ticket = 0


        event = Events(eventName, eventDescription, eventLocation, eventAddress, startDate,endDate, startTime, endTime, startTimeMin, endTimeMin, ticket)
        allEventr = root.child('events')
        allEventg = allEventr.get()
        try:
            for key in allEventg:
                if eventName[key]['Name'] == key:
                    flash('This event already exist')
                    return redirect(url_for('addRest'))
        except:
            pass

        currEvent = root.child('events/'+eventName)
        currEvent.update({
            'Name': event.get_eventName(),
            'Description': event.get_eventDescription(),
            'Location': event.get_eventLocation(),
            'Address': event.get_eventAddress(),
            'Start': event.get_startDate(),
            'End': event.get_endDate(),
            'Time Start': event.get_startTime(),
            'Time End': event.get_endTime(),
            'Min Start': event.get_startTimeMin(),
            'Min End': event.get_endTimeMin(),
            'ticket': event.get_ticket(),
            'People': 0,
            'User':user
        })
        flash('You have added a new event!')
        return redirect(url_for('home'))

    return render_template('events.html', form=form,proPic = session['proPic'],ongoing=ongoing,upcoming=upcoming,ended=ended,popEvent=popEvent )

@app.route('/events/<eventName>',methods=['POST','GET'])
def eventDet(eventName):
    try:
        proPic = session['proPic']
    except KeyError:
        session['proPic'] = ''

    eventName = eventName
    currEventr = root.child('events/'+eventName)
    currEventg = currEventr.get()

    form = EventForm(request.form)
    if request.method == 'POST':
        try:
            user = session['username']
        except:
            flash('You must be logged in to sign up for the event')
            return render_template('eventDet.html', currEventg=currEventg, proPic=proPic)
        goingEventr = root.child('events/'+eventName+'/Going')
        goingEventr.update({
            'Name':session['username']
        })
        flash('The event has been added to your profile successfully!')
        return redirect(url_for('userProfile'))
    return render_template('eventDet.html',currEventg=currEventg,proPic=proPic)





if __name__ == '__main__':
    socketio.run(app, debug=True)


