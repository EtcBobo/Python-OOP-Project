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
import feedparser
import string


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
    password = PasswordField('Password', [
        validators.Length(min=8),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    minPrice = IntegerField('Minimum Meal Budget (in Dollars)',[validators.DataRequired()])
    maxPrice = IntegerField('Maximum Meal Budget (in Dollars)',[validators.DataRequired()])
    foodType = SelectField(u'Preferred Food Type',
                           choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'), ('Western Food', 'Western Food'),
                                    ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                    ('None', 'None')])
    email = EmailField("Email",[validators.DataRequired()])
    sub = SelectMultipleField('Subsciption to weekly newsletter from The Foodie',
                               choices=[('I wish to receive weekly email from The Foodie.', 'I wish to receive weekly email from The Foodie.')],option_widget=widgets.CheckboxInput(),widget=widgets.ListWidget(prefix_label=False))



class RestForm(Form):
    name = StringField('Restaurant Name',[validators.DataRequired()])
    desc = TextAreaField('Desciption')
    location = SelectField(u'Location', choices=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South'),('Central','Central')])

    price = IntegerField(u'Average Meal Price (in Dollars)',[validators.DataRequired()])

    foodType = SelectField(u'Food Types',
                           choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'), ('Western Food', 'Western Food'),
                                    ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                    ('Any', 'Any')])
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
    pricef = IntegerField(u'Below input Price (in Dollars)',[validators.DataRequired()])
    openT = SelectField(u'Preferred Meal Time',
                        choices=[('12 PM', '12 PM'), ('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'),
                                 ('4 AM', '4 AM'),
                                 ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                 ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 AM', '12 AM'),
                                 ('1 PM', '1 PM'), ('2 PM', '2 PM'), ('3 PM', '3 PM'), ('4 PM', '4 PM'),
                                 ('5 PM', '5 PM'), ('6 PM', '6 PM'), ('7 PM', '7 PM'),
                                 ('8 PM', '8 PM'), ('9 PM', '9 PM'), ('10 PM', '10 PM'), ('11 PM', '11 PM')])
    foodType = SelectField(u'Food Types',
                           choices=[('Any', 'Any'),('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'),
                                    ('Western Food', 'Western Food'),
                                    ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food')])


class EventFilter(Form):
    fLocation = SelectField(u'Location',
                            choices=[('Any', 'Any'), ('North', 'North'), ('West', 'West'), ('East', 'East'),
                                     ('South', 'South'),
                                     ('Central', 'Central')])

    status = SelectField(u'Status',
                            choices=[('Any', 'Any'), ('Upcoming', 'Upcoming'), ('Ongoing', 'Ongoing'), ('Ended', 'Ended')])

    maxPrice = IntegerField(u'Maximum Budget (in Dollars)',[validators.DataRequired()])

class Feedbacks(Form):
    comments = TextAreaField('Comments')
    ratings = SelectField(u'Ratings of the restaurants (higher score means better rating)',choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])

class Sort(Form):
    sort = SelectField(u'Sort By:',
                          choices=[('Alphabetical Order', 'Alphabetical Order'), ('Lowest Price', 'Lowest Price'), ('Ratings (Higest to Lowest)', 'Ratings (Higest to Lowest)')])

class eSort(Form):
    sort = SelectField(u'Sort By:',
                          choices=[('Alphabetical Order', 'Alphabetical Order'), ('Lowest Price', 'Lowest Price'), ('Most Popular', 'Most Popular')])

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

class Forget(Form):
    name = StringField('Username', [validators.DataRequired()])
    email = EmailField("Email", [validators.DataRequired()])

class Forgetc(Form):
    code = StringField('Enter the validation code', [validators.DataRequired()])

class Reset(Form):
    password = PasswordField('New Password', [
        validators.Length(min=8),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

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

    # ------------------------------ NewsFeed ------------------------------
    def parseRSS(rss_url):
        return feedparser.parse(rss_url)

    def getHeadlines(rss_url):
        headlines = []

        feed = parseRSS(rss_url)
        for newsitem in feed['items']:
            headlines.append(newsitem)
        return headlines




    allheadlines = []

    newsurls = {'ladyiron':'http://www.ladyironchef.com/rss'}

    for key, url in newsurls.items():
        allheadlines.extend(getHeadlines(url))

    container = []

    for hl in allheadlines[0:3]:
        link = hl['link']

        date = hl['published']

        title = hl['title']

        content = hl['content']
        index = content[0]['value'].find('http')
        # finding the index for end of the url for the pic
        second_index = content[0]['value'].find('"', index)
        # print(content[0]['value'][index:second_index])
        image =content[0]['value'][index:second_index]


        news = {'title': title, 'link': link, 'date': date, 'image':image}
        container.append(news)


    # ------------------------------ Search ------------------------------
    nameList = []
    form = theSearch(request.form)
    if request.method == 'POST':

        name = form.name.data

        data = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")

        firebaseData = data.get('restaurants', None)
        firebaseDataEvent = data.get('events', None)

        for key in firebaseDataEvent:
            fireData = firebaseDataEvent[key]['Name']

            fireData_low = fireData.lower()

            if name.lower() in fireData_low:                    # if user input is same with words in firebase, the result will come out
                nameList.append(firebaseDataEvent[key])



        for key in firebaseData:
            fireData = firebaseData[key]['Name']

            fireData_low = fireData.lower()

            if name.lower() in fireData_low:                    #if user input is same with words in firebase, the result will come out
                nameList.append(firebaseData[key])

            #---------------------------------Old Codes---------------------------------------------------------#
            # fireData_sep = fireData_low.split()                 #split lowercase (for name that got space)
            # fireData_sep_first = fireData_low.split()[0]        #get first split value
            # fireData_2words = fireData_sep_first[0:2]           #get frist 2 words
            # fireData_3words = fireData_sep_first[0:3]           #get first 3 words
            # fireData_4words = fireData_sep_first[0:4]           #get first 4 words
            # fireData_5words = fireData_sep_first[0:5]           # get first 4 words
            # if fireData_low == name.lower():                    #exact match
            #     nameList.append(firebaseData[key])
            # if name.lower() in fireData_sep:                    #split value
            #     nameList.append(firebaseData[key])
            # if name.lower() in fireData_2words:                 #first 2 words
            #     nameList.append(firebaseData[key])
            # elif name.lower() in fireData_3words:               #first 3 words if use if got two same results
            #     nameList.append(firebaseData[key])
            # elif name.lower() in fireData_4words:               #first 4 words
            #     nameList.append(firebaseData[key])
            # elif name.lower() in fireData_5words:               #first 4 words
            #     nameList.append(firebaseData[key])

        session['filtered'] = nameList
        return redirect(url_for('view'))
    return render_template('home.html', recommend=randRec , form=form, proPic = proPic, hnp=list, container=container)



@app.route('/newsFeed')
def newsFeed():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic = ''

    def parseRSS(rss_url):
        return feedparser.parse(rss_url)

    def getHeadlines(rss_url):
        headlines = []

        feed = parseRSS(rss_url)
        for newsitem in feed['items']:
            headlines.append(newsitem)
        return headlines

    allheadlines = []

    newsurls = {'ladyiron':'http://www.ladyironchef.com/rss'}

    for key, url in newsurls.items():
        allheadlines.extend(getHeadlines(url))

    container = []

    for hl in allheadlines[0:15]:
        link = hl['link']

        date = hl['published']

        title = hl['title']

        content = hl['content']
        index = content[0]['value'].find('http')
        # finding the index for end of the url for the pic
        second_index = content[0]['value'].find('"', index)
        # print(content[0]['value'][index:second_index])
        image =content[0]['value'][index:second_index]

        news = {'title': title, 'link': link, 'date': date, 'image':image}
        container.append(news)

    return render_template('newsFeed.html', container=container,proPic=proPic )


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
    name = StringField('')   # line you will see above search form
    plswork = StringField('try')



@app.route('/filter',methods=['POST','GET'])
def filter():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''
    filterList = []
    form = FilterForm(request.form)
    if request.method == 'POST' and form.validate():
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

        if foodType != 'Any':
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


@app.route('/findEvent',methods=['POST','GET'])
def findEvent():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''
    filterList = []
    form = EventFilter(request.form)
    if request.method == 'POST' and form.validate():
        location = form.fLocation.data
        status = form.status.data
        maxPrice = form.maxPrice.data

        allEventr = root.child('events')
        allEventg = allEventr.get()


        for key in allEventg:
            if status == 'Any':
                filterList.append(allEventg[key])
            else:
                if allEventg[key]['Status'] == status:
                    filterList.append(allEventg[key])

        if location !='Any':
            i = 0
            while i < len(filterList):
                if filterList[i]['Location'] != location:
                    del filterList[i]
                    i = i - 1
                i = i + 1


        i = 0
        while i < len(filterList):
            if int(filterList[i]['ticket']) > int(maxPrice):
                del filterList[i]
                i = i - 1
            i = i + 1




        session['efiltered'] = filterList
        print(session['efiltered'])
        return redirect(url_for('viewEvent'))
    return render_template('findEvent.html', form=form,proPic=proPic)





@app.route('/viewEvent',methods=['POST','GET'])
def viewEvent():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''
    list = session['efiltered']
    listLen = len(list)


    form = eSort(request.form)
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
        elif sort == 'Most Popular':
            allRat = {}
            for key in list:
                allRat[key['Name']] = int(key['People'])

            newList = [(k, allRat[k]) for k in sorted(allRat, key=allRat.get)]
            newList2 = []
            for key in newList:
                for key2 in list:
                    if key[0] == key2['Name']:
                        newList2.insert(0,key2)
            list = newList2

        return render_template('viewEvent.html', events=list, lengthList=listLen, proPic=proPic, form=form)
    return render_template('viewEvent.html', events=list, lengthList = listLen,proPic=proPic,form=form)





@app.route('/map')
def map():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''
    list = []

    data = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
    firebaseData = data.get('restaurants', None)

    list.append(firebaseData)
    json_string = json.dumps(list)
    return render_template('map.html' , s_data = json_string, proPic=proPic)

# @app.route('/data')
# def data():
#     try:
#         proPic = session['proPic']
#     except KeyError:
#         proPic =''
#     list =[]
#     # data = firebase.FirebaseApplication("https://jsmap-a2929.firebaseio.com/")
#     # firebaseData = data.get('location', None)
#
#     data = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
#     firebaseData = data.get('locations', None)
#
#     list.append(firebaseData)
#
#     # for key in firebaseData:
#     #     data = firebaseData[key]
#     #     list.append(data)
#
#     json_string = json.dumps(list)
#
#
#
#     return render_template('data.html' , s_data = json_string, proPic = 'proPic')


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
    except KeyError:
        proPic =''

    try:
        user = session['username']
    except:
        return redirect(url_for('denied'))
    form = RestForm(request.form)
    restFirer = root.child('restaurants')
    restFireg = restFirer.get()
    count = len(restFireg)
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


        try:
            for key in restFireg:
                if name.lower == restFireg[key]['Name'].lower:
                    flash(u'This restaurant already exist','error')
                    return redirect(url_for('addRest'))
        except:
            pass
        if user == '':
            flash(u'You must be logged in to recommend a Restaurant','error')
            return redirect(url_for('addRest'))


        restFireu = root.child('restaurants/rest'+str(count))
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
        flash(u'You have added a new Restaurant!','success')

        return redirect(url_for('home'))
    return render_template('addRest.html', form=form,proPic=proPic,user=user,count=str(count))


@app.route('/userRegister',methods=['POST','GET'])
def userRegister():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''
    allUser = root.child('allUsers')
    allUserg = allUser.get()
    try:
        count = len(allUserg)
    except:
        count = 0


    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.user.data
        password = form.password.data
        minPrice = form.minPrice.data
        maxPrice = form.maxPrice.data
        foodType = form.foodType.data
        email = form.email.data
        sub = form.sub.data

        if minPrice > maxPrice:
            flash(u'The Minumum budget cannot exceed the Maximum budget','error')
            return redirect(url_for('userRegister'))

        if sub == 'I wish to receive weekly email from The Foodie.':
            sub = 'Yes'
        else:
            sub = 'No'



        reg = Registration(user,password,minPrice,maxPrice,foodType,email)


        for key in allUserg:
            if allUserg[key]['Username'] == user:
                flash(u'This username has already been used','error')
                return redirect(url_for('userRegister'))
            if allUserg[key]['Email'] == email and email != '':
                flash(u'This email has already been used','error')
                return redirect(url_for('userRegister'))

        if email == 'Yes':

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

        theUser = root.child('allUsers/user'+str(count))
        theUser.update({
            'Username': reg.get_user(),
            'Password': reg.get_password(),
            'minPrice': reg.get_minPrice(),
            'maxPrice':reg.get_maxPrice(),
            'Food Types': reg.get_foodType(),
            'Email':reg.get_email(),
            'sub':sub
        })

        flash(u'You have succesfully registered!','success')

        return redirect(url_for('home'))
    return render_template('userRegister.html', form=form,proPic=proPic,count=str(count))


@app.route('/bmi_calc', methods=['GET', 'POST'])
def bmi():
    def calc_bmi(weight, height):
        return round((weight / ((height / 100) ** 2)), 2)

    bmi = ''
    result = ''
    if request.method == 'POST' and 'weight' in request.form:
        weight = float(request.form.get('weight'))
        height = float(request.form.get('height'))
        bmi = calc_bmi(weight, height)
        if bmi < 18.5:
            result = "yOU ARE underweight!!"
        elif bmi > 25 and bmi < 30:
            result= "YoU are OverWeight!"
        elif bmi > 30:
            result = "You are obese!"
        else:
            result = "You are healthy!"
    return render_template("bmi_calc.html",
	                        bmi=bmi, result=result)


@app.route('/forget',methods=['POST','GET'])
def forget():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''

    form = Forget(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data

        theCheck = False

        allUserr = root.child('allUsers')
        allUserg = allUserr.get()
        for key in allUserg:
            if allUserg[key]['Username'] == name and allUserg[key]['Email'] == email:
                theCheck = True

        if theCheck == False:
            flash(u'Your Username and Email does not match', 'error')
            return redirect(url_for('forget'))



        def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

        code = id_generator()

        session['userReset'] = name


        email_user = 'omgnooopython@gmail.com'
        email_password = 'pythonnopython'
        email_send = email

        subject = 'Request for The Foodie account Password Reset'

        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        body = '\n Hi ' + name + '. A password reset request has been activated for your account. No Changes have been made to your account yet'\
                                 '\n \nPlease key in this confirmation code below in our webpage to verify the password reset request:'\
                                 '\nThe code is:'+code+'\n\nIf you did notrequest for a new password. Please ignore this email and contact us at thefoodie.newsletter@gmail.com''\n\nYours sincerely,''\n\nThe Foodie'

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

        session['code'] = code

        return redirect(url_for('forgetc'))

    return render_template('forget.html', form=form,proPic=proPic)


@app.route('/forgetc', methods=['POST', 'GET'])
def forgetc():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic = ''


    form = Forgetc(request.form)
    if request.method == 'POST':
        code = form.code.data

        if code == session['code']:
            return redirect(url_for('resetPass'))
        else:
            flash(u'Incorrect Validation Code','error')
            return redirect(url_for('forgetc'))


    return render_template('forgetc.html', form=form, proPic=proPic)


@app.route('/resetPass', methods=['POST', 'GET'])
def resetPass():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic = ''

    form = Reset(request.form)
    if request.method == 'POST' and form.validate():
        password = form.password.data

        allUserr = root.child('allUsers')
        allUserg = allUserr.get()
        for key in allUserg:
            if allUserg[key]['Username'] == session['userReset']:
                theUserr = root.child('allUsers/'+key)
        theUserr.update({
            'Password':password
        })
        flash(u'You have successfully changed your password','success')
        return redirect(url_for('home'))

    return render_template('resetPass.html', form=form, proPic=proPic)



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
                flash(u'You are successfully logged in','success')
                session['userPref'] = totalUsers[key]
                session['userDetail'] = totalUsers[key]
                session['proPic'] = totalUsers[key]['urlProfile']
                print(totalUsers[key])
                logCheck = True
                return redirect(url_for('home'))
        if logCheck == False:
            flash(u'Invalid Username or Password','error')
            session['logged_in'] = False

    return render_template('userLogin.html', form=form,proPic=proPic)

@app.route('/denied',methods=['POST','GET'])
def denied():
    try:
        proPic = session['proPic']
    except KeyError:
        proPic =''



    return render_template('denied.html',proPic=proPic)

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

    allRestr = root.child('restaurants')
    allRestg = allRestr.get()
    for key in allRestg:
        if allRestg[key]['Name'] == restName:
            restDetail =allRestg[key]
            restid = key

    allUserr =root.child('allUsers')
    allUserg = allUserr.get()



    """load all comments and ratings, and put all comments into a list"""
    try:
        counter = 0
        allComments = []
        allUsers = []
        allCommr = root.child('allComments')

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
            for key in allUserg:
                if allUsers[i] == allUserg[key]['Username']:
                   allPic.append(allUserg[key]['urlProfile'])


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

    print(allComments)
    try:
        commentLen = len(allComments)
    except:
        commentLen = 0

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
            theRestr = root.child('restaurants/'+restid)
            theRestr.update({
                'Average Rating':avgRatings,
                'Number of Raters':numRaters
            })
            print(avgRatings,numRaters)
            restDetail = theRestr.get()
            allUserr = root.child('allUsers')
            allUserg = allUserr.get()



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
                    for key in allUserg:
                        if allUsers[i] == allUserg[key]['Username']:
                            allPic.append(allUserg[key]['urlProfile'])

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

            try:
                commentLen = len(allComments)
            except:
                commentLen = 0



            return render_template('restDet.html', restDetail=restDetail, form=form, comments=allComments, users=allUsers,
                                   ratings=allRatings, proPic=proPic, pic=allPic,commentLen=commentLen,restid=restid)
        except:
            flash(u'You must login to be able to comment or rate restaurants','error')
            return render_template('restDet.html',restDetail = restDetail, form=form,comments=allComments,users=allUsers,ratings=allRatings,proPic=proPic, pic=allPic,commentLen=commentLen,restid=restid)

    return render_template('restDet.html',restDetail = restDetail, form=form,comments=allComments,users=allUsers,ratings=allRatings,proPic=proPic, pic=allPic,commentLen=commentLen,restid=restid)



@app.route('/eventEdit/<eventName>',methods=['POST','GET'])
def eventEdit(eventName):
    try:
        proPic = session['proPic']
    except KeyError:
        session['proPic'] = ''

    eventName = eventName
    theEventr = root.child('events')
    theEventg = theEventr.get()
    for key in theEventg:
        if eventName == theEventg[key]['Name']:
            theEvent = theEventg[key]
            eventid = key

    theEventr = root.child('events/'+eventid)

    class EventForm2(Form):
        eventDescription = TextAreaField('Desciption',default=theEvent['Description'])
        eventLocation = SelectField(u'Location',
                                    choices=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South'),
                                             ('Central', 'Central')],default=theEvent['Location'])
        eventAddress = TextAreaField('Place where your event is held',default=theEvent['Address'])
        ticket = IntegerField('Entry Fee',default=theEvent['ticket'])
        startDate = StringField('Start date (e.g.2018-01-12)*',default=theEvent['Start'])
        endDate = StringField('End date (e.g.2018-01-12)*',default=theEvent['End'])
        startTime = SelectField(u'Start Time(Hr)*',
                                choices=[('12 AM', '12 AM'), ('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'),
                                         ('4 AM', '4 AM'),
                                         ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                         ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                         ('1 PM', '1 PM'), ('2 PM', '2 PM'), ('3 PM', '3 PM'), ('4 PM', '4 PM'),
                                         ('5 PM', '5 PM'), ('6 PM', '6 PM'), ('7 PM', '7 PM'),
                                         ('8 PM', '8 PM'), ('9 PM', '9 PM'), ('10 PM', '10 PM'), ('11 PM', '11 PM')],default=theEvent['Time Start'])
        endTime = SelectField(u'End Time(Hr)*',
                              choices=[('12 AM', '12 AM'), ('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'),
                                       ('4 AM', '4 AM'),
                                       ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                       ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                       ('1 PM', '1 PM'), ('2 PM', '2 PM'), ('3 PM', '3 PM'), ('4 PM', '4 PM'),
                                       ('5 PM', '5 PM'), ('6 PM', '6 PM'), ('7 PM', '7 PM'),
                                       ('8 PM', '8 PM'), ('9 PM', '9 PM'), ('10 PM', '10 PM'), ('11 PM', '11 PM')],default=theEvent['Time End'])
        startTimeMin = SelectField(u'Start Time(Min)*',
                                   choices=[('00', '00'), ('05', '05'), ('10', '10'), ('15', '15'), ('20', '20'),
                                            ('25', '25'), ('30', '30'), ('35', '35'),
                                            ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55')],default=theEvent['Min Start'])
        endTimeMin = SelectField(u'End Time(Min)*',
                                 choices=[('00', '00'), ('05', '05'), ('10', '10'), ('15', '15'), ('20', '20'),
                                          ('25', '25'), ('30', '30'), ('35', '35'),
                                          ('40', '40'), ('45', '45'), ('50', '50'), ('55', '55')],default=theEvent['Min End'])

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
                flash(u'The End Date cannot be before the Start Date','error')
                return render_template('eventEdit.html', form=form, proPic=session['proPic'], eventName=eventName,eventid =eventid,
                                       theEvent=theEvent)
        except:
            flash(u'Please follow the example date format','error')
            return render_template('eventEdit.html', form=form, proPic=session['proPic'], eventName=eventName,theEvent=theEvent,eventid =eventid,)

        if ticket == '':
            ticket = 0


        theEventr.update({
            'Name':eventName,
            'Description': eventDescription,
            'Location': eventLocation,
            'Address': eventAddress,
            'Start': startDate,
            'End': endDate,
            'Time Start': startTime,
            'Time End': endTime,
            'Min Start': startTimeMin,
            'Min End': endTimeMin,
            'ticket': ticket,
            'People': theEvent['People'],
            'User': theEvent['User']
        })
        flash(u'You have successfully edited your Event!','success')
        return redirect(url_for('home'))

    return render_template('eventEdit.html', form=form, proPic=session['proPic'], eventName=eventName,theEvent=theEvent, eventid=eventid)


@app.route('/restEdit/<restName>',methods=['POST','GET'])
def restEdit(restName):
    try:
        proPic = session['proPic']
    except KeyError:
        session['proPic'] = ''
    restName = restName

    allRestr = root.child('restaurants')
    allRestg = allRestr.get()
    for key in allRestg:
        if allRestg[key]['Name'] == restName:
            restid = key
            restPic = allRestg[key]['urlRest']




    theRestr = root.child('restaurants/'+restid)
    theRestg = theRestr.get()



    class RestForm2(Form):
        desc = TextAreaField('Desciption', default=theRestg['Description'])

        location = SelectField(u'Location',
                               choices=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South'),
                                        ('Central', 'Central')],default=theRestg['Location'])

        price = IntegerField(u'Average Meal Price (in Dollars)',default=theRestg['Price'])
        foodType = SelectField(u'Food Types',
                               choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'),
                                        ('Western Food', 'Western Food'),
                                        ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                        ('Any', 'Any')],default=theRestg['Food Type'])
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
            'Name':restName,
            'Description': desc,
            'Location': location,
            'Price': price,
            'Food Type': foodType,
            'Opening Hours': openH,
            'Closing Hours': closingH,
            'Address': address,
            'User': theRestg['User'],
            'Average Rating': theRestg['Average Rating'],
            'Number of Raters': theRestg['Number of Raters'],
            'Days': theRestg['Days']
        })
        flash(u'You have successfully edited your restaurant!','success')


        return redirect(url_for('home'))
    return render_template('restEdit.html', form=form, proPic=session['proPic'],rest = theRestg,restPic=restPic,restid=restid)

@app.route('/userEdit',methods=['POST','GET'])
def userEdit():
    try:
        proPic = session['proPic']
    except KeyError:
        session['proPic'] =''
    class UserEdit(Form):
        password = PasswordField('New Password', [
            validators.Length(min=8),
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords must match')
        ])
        confirm = PasswordField('Repeat Password')
        minPrice = IntegerField('Minimum Meal Budget',[validators.DataRequired()],default=session['userDetail']['minPrice'])
        maxPrice = IntegerField('Maximum Meal Budget',[validators.DataRequired()], default=session['userDetail']['maxPrice'])
        foodType = SelectField(u'Preferred Food Type',
                               choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'),
                                        ('Western Food', 'Western Food'),
                                        ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                        ('None', 'None')], default=session['userDetail']['Food Types'])
        email = EmailField("Email", [validators.DataRequired()], default=session['userDetail']['Email'])
        sub = SelectMultipleField('Subsciption to weekly newsletter from The Foodie',
                                  choices=[('I wish to receive weekly email from The Foodie.',
                                            'I wish to receive weekly email from The Foodie.')],
                                  option_widget=widgets.CheckboxInput(), widget=widgets.ListWidget(prefix_label=False))

    form = UserEdit(request.form)
    allUserr = root.child('allUsers')
    allUserg= allUserr.get()
    for key in allUserg:
        if allUserg[key]['Username'] == session['username']:
            theKey=key


    if request.method == 'POST' and form.validate():
        email = form.email.data
        minPrice = form.minPrice.data
        maxPrice = form.maxPrice.data
        foodType = form.foodType.data
        password = form.password.data
        sub = form.sub.data
        if sub == 'I wish to receive weekly email from The Foodie.':
            sub = 'Yes'
        else:
            sub = 'No'

        if minPrice > maxPrice:
            flash(u'The Minumum budget cannot exceed the Maximum budget','error')
            return redirect(url_for('userEdit'))

        for key in allUserg:
            if allUserg[key]['Username'] != session['username']:
                if allUserg[key]['Email'] == email and email != '':
                    flash(u'This Email has already been used','error')
                    return redirect(url_for('userEdit'))

        userr = root.child('allUsers/'+theKey)
        userr.update({
            'Username': session['username'],
            'minPrice': minPrice,
            'maxPrice':maxPrice,
            'Food Types': foodType,
            'Email': email,
            'Password': password,
            'sub':sub
        })
        flash(u'You have succesfully edited your profile!','success')
        allUserr = root.child('allUsers')
        allUserg = allUserr.get()
        for key in allUserg:
            if session['username'] == allUserg[key]['Username']:
                session['userDetail'] = allUserg[key]
                session['proPic'] = allUserg[key]['urlProfile']

        return redirect(url_for('home'))
    return render_template('userEdit.html', form=form, user=session['userDetail'], proPic=session['proPic'], theKey=theKey)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have successfully logged out', 'success')
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
                if allEventg[key]['Going'][key2] == theUser['Username']:
                    goingEvent.append(allEventg[key])
        except:
            pass
    favRest = []
    try:
        allFavr= root.child('fav/'+theUser['Username'])
        allFavg = allFavr.get()
        for key in allFavg:
            for key2 in allRestg:
                if allRestg[key2]['Name'] == allFavg[key]:
                    favRest.append(allRestg[key2])
        print(favRest)
    except:
        pass

    return render_template('userProfile.html' , user = theUser, proPic = session['proPic'],allEdit=allEdit,allEvent=allEvent,goingEvent=goingEvent,favRest=favRest)


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
    try:
        for key in allEventg:
            if int(allEventg[key]['Start'][0:4]) > currYear:
                status.append('Upcoming')
            elif int(allEventg[key]['End'][0:4]) < currYear:
                status.append('Ended')
            elif int(allEventg[key]['Start'][0:4]) <= currYear and int(allEventg[key]['End'][0:4]) > currYear:
                status.append('Ongoing')
            elif int(allEventg[key]['Start'][0:4]) == currYear:

                if int(allEventg[key]['Start'][5:7]) > currMonth:
                    status.append('Upcoming')
                elif int(allEventg[key]['End'][5:7]) < currMonth:
                    status.append('Ended')
                elif int(allEventg[key]['Start'][5:7]) <= currMonth and int(allEventg[key]['End'][5:7]) > currMonth:
                    status.append('Ongoing')
                elif int(allEventg[key]['Start'][5:7]) == currMonth:

                    if int(allEventg[key]['Start'][8:]) > currDate:
                        status.append('Upcoming')
                    elif int(allEventg[key]['End'][8:]) < currDate:
                        status.append('Ended')
                    elif int(allEventg[key]['Start'][8:]) <= currDate and int(allEventg[key]['End'][8:]) > currDate:
                        status.append('Ongoing')

        for key in allEventg:
            eventr = root.child('events/'+key)
            eventr.update({
                'Status':status[count]
            })
            count = count +1

        print(status)

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
    except:
        pass


    theList = []
    ongoing = []
    upcoming = []
    ended = []
    popEvent = []

    allEventr = root.child('events')
    allEventg = allEventr.get()
    try:
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
    except:
        pass


    return render_template('events.html',proPic = session['proPic'],ongoing=ongoing,upcoming=upcoming,ended=ended,popEvent=popEvent)


@app.route('/addEvent',methods=['POST','GET'])
def addEvent():
    try:
        proPic = session['proPic']
    except KeyError:
        session['proPic'] =''

    try:
        user = session['username']
    except:
        return redirect(url_for('denied'))


    allEventr = root.child('events')
    allEventg = allEventr.get()
    try:
        numEvent = len(allEventg)
    except:
        numEvent = 0

    for key in allEventg:
        if allEventg[key]['Name'] == 'placeholder':
            numEvent = len(allEventg) - 1



    form = EventForm(request.form)
    if request.method == 'POST' and form.validate():
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
                flash(u'The End Date cannot be before the Start Date','error')
                return redirect(url_for('addEvent'))
        except:
            flash(u'Please follow the example date format','error')
            return redirect(url_for('addEvent'))

        if startTime == '12 AM':
            startHour = 0
        elif startTime == '12 PM':
            startHour = 12
        elif startTime[-2:] == 'AM':
            startHour = int(startTime[0:2])
        elif startTime[-2:] == 'PM':
            startHour = int(startTime[0:2]) + 12

        if endTime == '12 AM':
            endHour = 0
        elif endTime == '12 PM':
            endHour = 12
        elif endTime[-2:] == 'AM':
            endHour = int(startTime[0:2])
        elif endTime[-2:] == 'PM':
            endHour = int(startTime[0:2]) + 12

        if startDate == endDate:
            if startHour > endHour:
                flash(u'The Start Time cannot be later than the End Time!','error')
                return redirect(url_for('addEvent'))
            elif startHour == endHour:
                if int(startTimeMin) > int(endTimeMin):
                    flash(u'The Start Time cannot be later than the End Time!','error')
                    return redirect(url_for('addEvent'))

        if ticket == '':
            ticket = 0

        event = Events(eventName, eventDescription, eventLocation, eventAddress, startDate, endDate, startTime, endTime,
                       startTimeMin, endTimeMin, ticket)
        allEventr = root.child('events')
        allEventg = allEventr.get()
        try:
            for key in allEventg:
                if eventName.lower == allEventg[key]['Name'].lower:
                    flash(u'This event already exist','error')
                    return redirect(url_for('addRest'))
        except:
            pass

        theBreak = False
        while theBreak == False:
            try:
                allEventr = root.child('events')
                allEventg = allEventr.get()
                for key in allEventg:
                    if allEventg[key]['Name'] == 'placeholder':
                        eventKey = key
                        theBreak = True
            except:
                pass


        currEvent = root.child('events/' + eventKey)
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
            'User': user
        })
        flash(u'You have added a new event!','success')
        return redirect(url_for('home'))
    return render_template('addEvent.html', form=form,proPic=session['proPic'], numEvent=str(numEvent))

@app.route('/eventDet/<eventName>',methods=['POST','GET'])
def eventDet(eventName):
    try:
        proPic = session['proPic']
    except KeyError:
        session['proPic'] = ''

    eventName = eventName
    currEventr = root.child('events')
    currEventg = currEventr.get()
    for key in currEventg:
        if currEventg[key]['Name'] == eventName:
            currEvent = currEventg[key]
            eventKey = key

    form = EventForm(request.form)
    if request.method == 'POST':
        try:
            user = session['username']
        except:
            flash(u'You must be logged in to sign up for the event','error')
            return render_template('eventDet.html', currEventg=currEventg, proPic=proPic)
        goingEventr = root.child('events/'+eventKey+'/Going')
        goingEventr.update({
            session['username']:session['username']
        })
        flash(u'The event has been added to your profile successfully!','success')
        return redirect(url_for('userProfile'))
    return render_template('eventDet.html',currEventg=currEvent,proPic=proPic)


if __name__ == '__main__':
    socketio.run(app, debug=True)


