from flask import Flask, session, render_template, redirect, url_for, escape, request, json, abort
import os
import sys
import MySQLdb
import datetime
from werkzeug.utils import secure_filename
import dbconnection
import calendarf
from user import User
from event import Event

# EB looks for an 'application' callable by default.
application = Flask(__name__)
#instantiate DBManager
db = dbconnection.DBManager()

@application.route('/')
def hello():
    return render_template('index.html')

@application.route('/u/')
@application.route('/u/<name>')
def user(name=None):
    # This what the template needs to show all the data on the site
    if 'userInfo' in session:
        user = {'name': session['userInfo']['name'],
                'title': session['userInfo']['title'],
                'rating': [{'title': "Support", 'rating': session['userInfo']['rating']},
                        {'title': "Apple", 'rating': session['userInfo']['rating']},
                        {'title': "Potato", 'rating': session['userInfo']['rating']}],
                'pictureUrl': session['userInfo']['pictureUrl'],
                'events' : session['userInfo']['events']}
    else:
        user = {
        'name': name,
        'title': 'User',
        'rating': [{'title': "Support", 'rating': 9},
            {'title': "Apple", 'rating': 5},
            {'title': "Potato", 'rating': 8}],
        'pictureUrl': 'https://asimshrestha2.github.io/portfoliov2/imgs/Asim_Ymir.png',
        'events': [{'name': "Dance", 'description': "This is a description for the dance event that is going on",
            'pictureUrl': 'http://orig13.deviantart.net/ac10/f/2015/100/c/4/render_4_edited_by_asimshrestha2-d8p8rbi.png'},
            {'name': "Dance No. 2", 'description': "This is a description for the dance event 2 that is going on",
            'pictureUrl': 'http://orig13.deviantart.net/ac10/f/2015/100/c/4/render_4_edited_by_asimshrestha2-d8p8rbi.png'},
            {'name': "Dance No. 3", 'description': "This is a description for the dance event 3 that is going on",
            'pictureUrl': 'http://orig13.deviantart.net/ac10/f/2015/100/c/4/render_4_edited_by_asimshrestha2-d8p8rbi.png'}]
        }
    return render_template('profile.html', user = user, name=name)


@application.route('/e/')
@application.route('/e/<name>')
def event(name=None):
    if name == None:
        return redirect(url_for('hello'))
    else:
        event = {
            'name': name,
            'location': "Towson University, Towson, MD",
            'host': "Asim Shrestha",
            'description': "This is the description from Python",
            'pictureUrl': 'https://asimshrestha2.github.io/imgs/content/environment.png'
        }
        return render_template('eventpage.html', event=event)

# Function for all the login user page
@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #parse in the form data, make sure strings aren't SQL injection
        username = checkInput(request.form['username'])
        password = checkInput(request.form['password'])
        #execute query to see if valid username password combo
        result = db.executeQuery(db.loginQuery.format(username, password))
        #if sucessful will continue on, else will throw error inside executeQuery
        #just some debug stuff for now
        if result is not None:
            #create some session variables with data that will be used frequently
            result = result[0]
            eQRes = db.executeQuery(db.eventAttendingQuery.format(result[0]))
            #lets populate our user class with the event information
            events = []
            if eQRes is not None: #if we don't have any we don't have to do this
                for event in eQRes:
                    #gets result of location query which returns school address and facility name
                    locationQueryRes = db.executeQuery(db.locQuery.format(event[2],event[3]))
                    if locationQueryRes is not None:
                        locationQueryRes = locationQueryRes[0]
                        #create actual location string to be displayed
                        location = locationQueryRes[0] + "in facility: " + locationQueryRes[1]
                        events.append(Event(event[1], event[11], "http://static.zerochan.net/Stardust.Dragon.full.1878025.jpg", db.executeQuery(db.locQuery.format(event[3]))[0][0], event[4]))
            userInfo = User(result[1], result[5], 0, 'https://images3.alphacoders.com/761/thumb-350-761779.jpg', events)
            #we can't save classes in sessions, but we can turn them into dictionaries
            session['userInfo'] = userInfo.serialize()
            session['username'] = username
            session['userType'] = result[5]
            return url_for('user', name = username)
        #else we have wrong password
        return "-1"
    else:
        return render_template('login.html')

#TODO: Change logout return
@application.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('userType', None)
    session.pop('userInfo', None)
    return redirect(url_for('hello'))

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        #parse in the form data, make sure strings aren't SQL injection
        name = checkInput(request.form['firstname'] + " " + request.form['lastname'])
        email = checkInput(request.form['email'])
        phone_num = checkInput(request.form['phone'])
        uzip = checkInput(request.form['zip'])
        user_type = 'Public'
        username = checkInput(request.form['username'])
        password = checkInput(request.form['password'])
        user_address = checkInput(request.form['address'])
        #execute query to see if valid username password combo
        row1 = db.executeQuery(db.registerQuery.format(name,email,phone_num,uzip,user_type,username,password,user_address,0))
        #create some session variables with data that will be used frequently
        if row1:
            # Returns if no user
            return "-1"
        else:
            #if sucessful will continue on, else will throw error inside executeQuery
            #just some debug stuff for now
            #, file=sys.stderr
            session['username'] = username
            session['userType'] = 'Public'
            return url_for('hello')
    else:
        return render_template('signup.html')

# set the secret key.  keep this really secret:
#TODO: Change secret_key
application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@application.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'POST':
        res = calendarf.getweekevents()
        print(res)
        response = application.response_class(
            response=json.dumps(res),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        return render_template('calendar.html')

#Search Page
@application.route('/search')
def search():
    return(render_template('search.html'))

#TODO: Add more to create event
@application.route('/createevent', methods=['GET', 'POST'])
def createevent():
    if request.method == 'POST':
        return "1"
    else:
        if session.get('userType') != None:
            return render_template('createevent.html')
        else:
            abort(404)

@application.route('/getschools', methods=["POST"])
def getschools():
    cols = ["school_id", "school_name", "school_address"]
    colStr = ""
    for i in range(len(cols)):
        if(i != len(cols) - 1):
            colStr += cols[i] + ', '
        else:
            colStr += cols[i]
    query = "select " + colStr + " from school;"
    schools = db.executeQuery(query)
    res = []
    for school in schools:
        sc = {}
        for i in range(len(school)):
            sc[cols[i]]=school[i]
        res.append(sc)
    response = application.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )
    return response

@application.route('/getfacilitiesforschool', methods=["POST"])
def getfacilitiesforschool():
    school_id = request.form['school_id']
    cols = ["facility_id", "facility_name", "capacity", "time_open", "time_close", "facility_rent"]
    colStr = ""
    for i in range(len(cols)):
        if(i != len(cols) - 1):
            colStr += cols[i] + ', '
        else:
            colStr += cols[i]
    query = "select " + colStr + " from facility where school_id="+school_id+";"
    facilities = db.executeQuery(query)
    res = []
    for facility in facilities:
        res.append({cols[0]:facility[0], cols[1]:facility[1], cols[2]:facility[2], cols[3]: str(facility[3]),
        cols[4]: str(facility[4]), cols[5]: float(facility[5])})
    response = application.response_class(
        response=json.dumps(res),
        status=200,
        mimetype='application/json'
    )
    return response

@application.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@application.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(application.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

def checkInput(stringInput):
    #remove whitespace
    stringInput.strip()
    return stringInput
    #remove slashes
    #stringInput.decode('string_ecape')

# TODO: Handle the Money API

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
