import firebase_admin
from Registration import Registration
from firebase_admin import credentials, db
from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, PasswordField, IntegerField, validators
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
    price = StringField('Price Range')
    foodType = SelectField(u'Food Types',
                           choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'), ('Western Food', 'Western Food'),
                                    ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                    ('None', 'None')])



class RestForm(Form):
    name = StringField('Restaurant Name',[validators.DataRequired()])
    desc = StringField('Desciption')
    location = SelectField(u'Location', choices=[('North', 'North'), ('West', 'West'), ('East', 'East'), ('South', 'South')])
    price = StringField('Average Price')
    foodType = SelectField(u'Food Types',
                           choices=[('Halal', 'Halal'), ('Vegetarian', 'Vegetarian'), ('Western Food', 'Western Food'),
                                    ('Chinese Food', 'Chinese Food'), ('Healthy Food', 'Healthy Food'),
                                    ('None', 'None')])
    openH = StringField('Opening Hours')
    address = StringField('Address')
    comment = StringField('Comments')



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
        openH = form.openH.data


        restFire = firebase.FirebaseApplication("https://python-oop.firebaseio.com/")
        totalRest = restFire.get('restaurants',None)
        for key in totalRest:
            if location == totalRest[key]['Location'] or location == '':
                filterList.append(totalRest[key])
        if price != '':
            for key in filterList:
                if price != filterList[key]['Price']:
                    filterList.remove(filterList[key])

        if foodType != 'None':
            for key in filterList:
                if foodType != filterList[key]['Food Type']:
                    filterList.remove(filterList[key])

        if openH != '':
            for key in filterList:
                if openH != filterList[key]['Opening Hours']:
                    filterList.remove(filterList[key])
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
    if request.method == 'POST' and form.validate():
        name = form.name.data
        desc = form.desc.data
        location = form.location.data
        price = form.price.data
        foodType = form.foodType.data
        openH = form.openH.data
        address = form.address.data
        comment = form.comment.data
        res = Restaurant(name,desc,location,price,foodType,openH,address,comment)

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
