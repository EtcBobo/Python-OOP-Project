import firebase_admin
from Registration import Registration
from firebase_admin import credentials, db
from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, IntegerField, validators, SelectMultipleField
from firebase import firebase
from Restaurant import Restaurant

cred = credentials.Certificate('cred/python-oop-firebase-adminsdk-87ty7-eefcb6bc40.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://python-oop.firebaseio.com/'
})

root = db.reference()
app = Flask(__name__)





class RegisterForm(Form):
    user = StringField('Username',[validators.DataRequired()])
    password = PasswordField("Password",[validators.DataRequired()])
    price = StringField('Preferred Price Range')
    foodType = SelectMultipleField(u'Preferred Food Type',
                           choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'), ('Western Food', 'Western Food'),
                                    ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                    ('None', 'None')])



class RestForm(Form):
    name = StringField('Restaurant Name',[validators.DataRequired()])
    desc = TextAreaField('Desciption')
    location = SelectField(u'Location', choices=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South'),('Central','Central')])
    price = StringField('Average Price')
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
                           choices=[('12 AM', '12 AM'),('1 AM', '1 AM'), ('2 AM', '2 AM'), ('3 AM', '3 AM'), ('4 AM', '4 AM'),
                                    ('5 AM', '5 AM'), ('6 AM', '6 AM'), ('7 AM', '7 AM'), ('8 AM', '8 AM'),
                                    ('9 AM', '9 AM'), ('10 AM', '10 AM'), ('11 AM', '11 AM'), ('12 PM', '12 PM'),
                                    ('1 PM', '1 PM'),('2 PM', '2 PM'),('3 PM', '3 PM'),('4 PM', '4 PM'),('5 PM', '5 PM'),('6 PM', '6 PM'),('7 PM', '7 PM'),
                                    ('8 PM', '8 PM'),('9 PM', '9 PM'),('10 PM', '10 PM'),('11 PM', '11 PM'),])
    address = TextAreaField('Address')
    comment = TextAreaField('Comments')



@app.route('/')
def home():
    return render_template('home.html')


@app.route('/filter',methods=['POST','GET'])
def filter():
    filterList = []
    form = RestForm(request.form)
    if request.method == 'POST':
        location = form.location.data
        price = form.price.data
        foodType = form.foodType.data
        openT = form.openT.data


        restFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        totalRest = restFire.get('restaurants',None)

        for key in totalRest:
            if totalRest[key]['Opening Hours'][-2:] == 'PM':
                openH = int(totalRest[key]['Opening Hours'][0:2]) + 12
            else:
                openH = int(totalRest[key]['Opening Hours'][0:2])

            if totalRest[key]['Closing Hours'][-2:] == 'PM':
                closingH = int(totalRest[key]['Closing Hours'][0:2]) + 12
            else:
                closingH = int(totalRest[key]['Closing Hours'][0:2])

            if openT[-2:] == 'PM':
                openT1 = int(openT[0:2]) +12
            else:
                openT1 = int(openT[0:2])

            if openH <= openT1 < closingH or openT1 < closingH < openH or openT1 > openH > closingH or closingH == openH:
                filterList.append(totalRest[key])

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
                if filterList[i]['Food Types'] != foodType:
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
    return render_template('viewRest.html', Restaurant=list)

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
        comment = form.comment.data

        res = Restaurant(name,desc,location,price,foodType,openH,closingH,address,comment)

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
            'Comments': res.get_comment()

        })

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
        reg = Registration(user,password,price,foodType)


        userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        allUser = userFire.get('allUsers',None)
        for key in allUser:
            if allUser[key]['Username'] == user:
                flash('This username has already been used')
                return redirect(url_for('userRegister'))
        try:
            totalUsers = userFire.get('allUsers',None)
            count = len(totalUsers)
        except TypeError:
            count = 0
        userFire.put('allUsers','user'+str(count),{
            'Username': reg.get_user(),
            'Password': reg.get_password(),
            'Price': reg.get_price(),
            'Food Types': reg.get_foodType()

        })
        flash('You are succesfully registered')
        return redirect(url_for('home'))
    return render_template('userRegister.html', form=form)


@app.route('/userLogin',methods=['POST','GET'])
def userLogin():
    logCheck = False
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.user.data
        password = form.password.data

        userFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        totalUsers = userFire.get('allUsers',None)
        for key in totalUsers:
            if password == totalUsers[key]['Password'] and user == totalUsers[key]['Username']:
                session['logged_in'] = True
                session['username'] = totalUsers[key]['Username']
                flash('You were successfully logged in')
                logCheck = True
                return redirect(url_for('home'))
        if logCheck == False:
            flash('Invalid Username or Password')
            session['logged_in'] = False

    return render_template('userLogin.html', form=form)


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
    app.secret_key = 'secret123'
    app.run(debug=True)
