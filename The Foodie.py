import firebase_admin
from Registration import Registration
from firebase_admin import credentials, db
from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, IntegerField, validators, SelectMultipleField
from wtforms.fields.html5 import EmailField
from firebase import firebase
from Restaurant import Restaurant
from flask_googlemaps import GoogleMaps,Map
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from flask_socketio import SocketIO, emit
import random
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map

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


# GoogleMaps(app, key="AIzaSyAN-25Ihf-_ndHtyzHEXF2SGjI6U-WqQKc")

GoogleMaps(app, key="AIzaSyCrGeXVb96USi1ujzqQ7wlCwc_8LzUB-yY")



class RegisterForm(Form):
    user = StringField('Username',[validators.DataRequired()])
    password = PasswordField("Password",[validators.DataRequired()])
    passwordC = PasswordField("Confirm Password",[validators.DataRequired()])
    price = StringField('Preferred Price Range')
    foodType = SelectField(u'Preferred Food Type',
                           choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'), ('Western Food', 'Western Food'),
                                    ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                    ('None', 'None')])
    email = EmailField("Email", [validators.optional()])



class RestForm(Form):
    name = StringField('Restaurant Name',[validators.DataRequired()])
    desc = TextAreaField('Desciption')

    location = SelectField(u'Location', choices=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South'),('Central','Central')])
    fLocation = SelectField(u'Location',
                           choices=[('Any','Any'),('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South'),
                                    ('Central', 'Central')])

    price = StringField('Average Price',[validators.DataRequired()])
    foodType = SelectField(u'Food Types',
                           choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'), ('Western Food', 'Western Food'),
                                    ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                    ('None', 'None')])
    openH = SelectField(u'Opening Hours',
                           choices=[('12 AM', '12 AM'),('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'), ('4 AM', '4 AM'),
                                    ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                    ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                    ('1 PM', '1 PM'),('2 PM', '2 PM'),('3 PM', '3 PM'),('4 PM', '4 PM'),('5 PM', '5 PM'),('6 PM', '6 PM'),('7 PM', '7 PM'),
                                    ('8 PM', '8 PM'),('9 PM', '9 PM'),('10 PM', '10 PM'),('11 PM', '11 PM')])
    closingH = SelectField(u'Closing Hours',
                           choices=[('12 AM', '12 AM'),('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'), ('4 AM', '4 AM'),
                                    ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                    ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                    ('1 PM', '1 PM'),('2 PM', '2 PM'),('3 PM', '3 PM'),('4 PM', '4 PM'),('5 PM', '5 PM'),('6 PM', '6 PM'),('7 PM', '7 PM'),
                                    ('8 PM', '8 PM'),('9 PM', '9 PM'),('10 PM', '10 PM'),('11 PM', '11 PM'),])
    openT = SelectField(u'Operating Time',
                           choices=[('12 PM', '12 PM'),('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'), ('4 AM', '4 AM'),
                                    ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                    ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 AM', '12 AM'),
                                    ('1 PM', '1 PM'),('2 PM', '2 PM'),('3 PM', '3 PM'),('4 PM', '4 PM'),('5 PM', '5 PM'),('6 PM', '6 PM'),('7 PM', '7 PM'),
                                    ('8 PM', '8 PM'),('9 PM', '9 PM'),('10 PM', '10 PM'),('11 PM', '11 PM')])
    address = TextAreaField('Address')

class Feedbacks(Form):
    comments = TextAreaField('Comments')
    ratings = SelectField(u'Ratings of the restaurants (higher score means better rating)',choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])


# @app.route('/findgps')
# def findgps():
#     return render_template('findgps.html')

@app.route("/location")
def mapview():
    map = Map(
        identifier="map",
        style=(
            "height:50%;"
            "width:100%;"
            "top:100px;"
            "position:absolute;"
        ),
        lat=1.3786539,
        lng=103.8493234,
        markers=[
            {
                'lat':  1.372121,
                'lng':  103.846678,
                'infobox': (
                    "<h3>Ang Mo Kio Market & Food Centre</h3>"
                    "<p>Address: 724 Ang Mo Kio Ave 6, Singapore 560724</p>" 
                    "<p>Hours: 7AM–9PM</p>" 
                    "<p>Phone: 6225 5632</p>"
                    "<img src='//placehold.it/50'>")
            },
            {
                'lat': 1.380936,
                'lng': 103.840664,
                'infobox': (
                    "<h3>Ang Mo Kio 628 Market</h3>" 
                    "<p>Address: 724 Ang Mo Kio Ave 6, Singapore 560724</p>" 
                    "<p>Hours: Wednesday\t6:30AM–1:30PM</p>" 
                    "<p>Thursday\t6:30AM–1:30PM</p>" 
                    "<p>Friday\t6:30AM–1:30PM</p>" 
                    "<p>Saturday\t6:30AM–1:30PM</p>" 
                    "<p>Sunday\t6:30AM–1:30PM</p>" 
                    "<p>Monday\tClosed</p>" 
                    "<p>Tuesday\t6:30AM–1:30PM</p>" 
                    "<p>Phone: 9067 5142</p>"
                    "<img src='//placehold.it/50'>"
                )
            }
        ]
    )
    return render_template('findgps.html', map=map)



@app.route('/', methods=['POST', 'GET'])
def home():
    try:
        userPref = session['userPref']
    except KeyError:
        userPref = {'Food Types':'None'}
    print(userPref)
    recommend = []
    randRec = []
    restFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
    totalRest = restFire.get('restaurants', None)
    for key in totalRest:
        if totalRest[key]['Food Type'] == userPref['Food Types'] or userPref['Food Types']== 'None':
            recommend.append(totalRest[key])
    option1, option2, option3 = random.sample(range(0, len(recommend)), 3)
    randRec.append(recommend[option1])
    randRec.append(recommend[option2])
    randRec.append(recommend[option3])


    nameList = []
    form = theSearch(request.form)
    if request.method == 'POST':

        name = form.name.data

        data = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        firebaseData = data.get('restaurants', None)

        for key in firebaseData:
            if firebaseData[key]['Name'].lower() == name.lower():
                nameList.append(firebaseData[key])
        session['filtered'] = nameList
        return redirect(url_for('view'))
    return render_template('home.html', recommend=randRec , form=form)


@app.route('/chat')
def hello():
  return render_template( '/chat.html' )


def messagereceived():
  print( 'message was received!!!' )

@socketio.on( 'my event' )
def handle_my_custom_event( json ):
  print( 'recived my event: ' + str( json ) )
  socketio.emit( 'my response', json, callback=messagereceived())


class theSearch(Form):
    name = StringField('Enter the Food You Want')   # line you will see above search form
    plswork = StringField('try')



@app.route('/filter',methods=['POST','GET'])
def filter():
    filterList = []
    form = RestForm(request.form)
    if request.method == 'POST':
        location = form.fLocation.data
        price = form.price.data
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



        if price != '':
            i = 0
            while i < len(filterList):
                if int(filterList[i]['Price']) > int(price):
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
    return render_template('filter.html', form=form)

@app.route('/viewRest',methods=['POST','GET'])
def view():

    list = session['filtered']
    listLen = len(list)
    print(list)

    return render_template('viewRest.html', Restaurant=list, lengthList = listLen)





@app.route('/addRest',methods=['POST','GET'])
def addRest():
    form = RestForm(request.form)
    if request.method == 'POST':
        name = form.name.data
        desc = form.desc.data
        location = form.location.data
        price = form.price.data
        foodType = form.foodType.data
        openH = form.openH.data
        closingH = form.closingH.data
        address = form.address.data
        if price == '':
            flash('Please enter an average price for the restaurant')
            return redirect(url_for('addRest'))

        res = Restaurant(name,desc,location,price,foodType,openH,closingH,address)

        restFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        try:
            totalRest = restFire.get('restaurants', None)
            count = len(totalRest)
        except TypeError:
            count = 0
        restFire.put('restaurants', 'rest' + str(count), {
            'Name': res.get_name(),
            'Description': res.get_description(),
            'Location': res.get_location(),
            'Price': res.get_price(),
            'Food Type': res.get_foodType(),
            'Opening Hours': res.get_openH(),
            'Closing Hours': res.get_closingH(),
            'Address': res.get_address(),


        })
        flash('You have added a new Restaurant!')
        return redirect(url_for('home'))
    return render_template('addRest.html', form=form)


@app.route('/userRegister',methods=['POST','GET'])
def userRegister():

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
        return redirect(url_for('home'))
    return render_template('userRegister.html', form=form)


@app.route('/userLogin',methods=['POST','GET'])
def userLogin():
    logCheck = False
    form = RegisterForm(request.form)
    if request.method == 'POST':
        user = form.user.data
        password = form.password.data
        userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        totalUsers = userFire.get('allUsers',None)
        for key in totalUsers:
            if password == totalUsers[key]['Password'] and user == totalUsers[key]['Username']:
                session['logged_in'] = True
                session['username'] = totalUsers[key]['Username']
                flash('You are successfully logged in')
                session['userPref'] = totalUsers[key]
                logCheck = True
                return redirect(url_for('home'))
        if logCheck == False:
            flash('Invalid Username or Password')
            session['logged_in'] = False

    return render_template('userLogin.html', form=form)

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
    restName = restName
    form = Feedbacks(request.form)
    restFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
    totalRest = restFire.get('restaurants', None)
    for key in totalRest:
        if restName == totalRest[key]['Name']:
            restDetail = totalRest[key]
    feedback = restFire.get(restName, None)
    newFeed = []
    try:
        for key in range(int(len(feedback) / 3)):
            newFeed.append({'User': feedback['UserNo' + str(key)]['User'],
                            'Comment': feedback['CommentNo' + str(key)]['Comment'],
                             'Rating': int(feedback['RatingNo' + str(key)]['Rating'])})

    except TypeError:
        pass


    if request.method == 'POST':
        comments = form.comments.data
        ratings = form.ratings.data
        try:
            try:
                totalCom = restFire.get(restName,None)
                count = int(len(totalCom) / 3)
            except TypeError:
                count = 0
            restFire.put(restName,'CommentNo'+str(count),{
                'Comment': comments
            })
            restFire.put(restName,'RatingNo'+str(count), {
                'Rating': ratings
            })
            restFire.put(restName,'UserNo'+str(count) ,{
                'User': session['username']
            })
            restFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
            totalRest = restFire.get('restaurants', None)
            for key in totalRest:
                if restName == totalRest[key]['Name']:
                    restDetail = totalRest[key]
            feedback = restFire.get(restName, None)
            newFeed = []
            try:
                for key in range(int(len(feedback) / 3)):
                    newFeed.append({'User': feedback['UserNo' + str(key)]['User'],
                                    'Comment': feedback['CommentNo' + str(key)]['Comment'],
                                    'Rating': int(feedback['RatingNo' + str(key)]['Rating'])})

            except TypeError:
                pass
            return render_template('restDet.html', restDetail=restDetail, form=form, feedback=newFeed)
        except KeyError:
            flash('You must login to be able to comment or rate restaurants')
            return render_template('restDet.html', restDetail=restDetail, form=form, feedback=newFeed)
    return render_template('restDet.html',restDetail = restDetail, form=form,feedback=newFeed)

@app.route('/userEdit',methods=['POST','GET'])
def userEdit():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        user = form.user.data
        email = form.email.data
        price = form.price.data
        foodType = form.foodType.data
        password = form.password.data
        passwordC = form.passwordC.data
        if password != passwordC:
            flash('The passwords does not match')
            return redirect(url_for('userEdit'))
        userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        allUser = userFire.get('allUsers', None)
        for key in allUser:
            if allUser[key]['Username'] == user:
                flash('This username has already been used')
                return redirect(url_for('userEdit'))
            try:
                if allUser[key]['Email'] == email and email != '':
                    flash('This email has already been used')
                    return redirect(url_for('userEdit'))
            except KeyError:
                email = ''
        for key in allUser:
            if allUser[key]['Username'] == session['username']:
                userid = key
        userFire.put('allUsers', userid, {
            'Username': user,
            'Price': price,
            'Food Types': foodType,
            'Email': email,
            'Password': password
        })
        session['username'] = user
        flash('You have succesfully edited your profile!')
        return redirect(url_for('home'))
    return render_template('userEdit.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('userLogin'))

@app.route('/userProfile')
def userProfile():
    userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
    totalUsers = userFire.get('allUsers', None)
    for key in totalUsers:
        if totalUsers[key]['Username'] == session['username']:
            theUser = totalUsers[key]

    return render_template('userProfile.html' , user = theUser)




if __name__ == '__main__':
    socketio.run(app, debug=True)

