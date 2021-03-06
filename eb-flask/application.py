from flask import Flask, session, render_template, redirect, url_for, escape, request, json, abort
import os
import sys
import MySQLdb
import datetime
import stripe
from werkzeug.utils import secure_filename
from dbconnection import DBManager
from stripeconnection import StripeManager
import calendarf
import eventmanager
import urllib.parse as urllib
from user import User
from event import Event

# EB looks for an 'application' callable by default.
application = Flask(__name__)
#instantiate DBManager
db = DBManager()
stripeM = StripeManager()
#set secret key
@application.route('/')
def hello():
    se = None if session.get('userstate') == None else eventmanager.geteventswithstate(session.get('userstate'))
    return render_template('index.html', fe = eventmanager.getfeaturedevent(), se = se)

# set the secret key.  keep this really secret:
#TODO: Change FLASK secret_key
application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@application.route('/u/')
@application.route('/u/<name>')
def user(name=None):
    # This what the template needs to show all the data on the site
    userres = db.executeQuery(db.selectUserQuery.format(str(name)))
    user = None if userres is None else userres[0]

    evertres = db.executeQuery(db.selectUserEventQuery.format(str(user[0])))
    events = None if evertres is None else evertres



    user = {'name': user[1], 'title': user[5],
            'rating': [{'title': "User Rating", 'rating': user[9]}],
            'pictureUrl': 'https://asimshrestha2.github.io/portfoliov2/imgs/Asim_Ymir.png',
            'events' : events}
    if(user[5] == 'School'):
        facilities = db.executeQuery(db.getFacilitiesQuery.format(str(user[10])))
        user['fs'] = facilities
        print(userr)
    return render_template('profile.html', user = userr, name=name)


@application.route('/e/')
@application.route('/e/<int:id>/<name>', methods=['GET', 'DELETE'])
def event(id=None, name=None):
    if request.method == 'DELETE':
        query = "select host_id from event where event_id =" + str(id) + " and event_name='"+ name +"';"
        result = db.executeQuery(query)
        if result:
            host_id = result[0][0]
            db.executeQuery("delete from event where event_id="+ str(id) + " and event_name='"+ name + "' and host_id="+ str(host_id) +";")
            return '1'
        else:
            return '-1'
    else:
        if name == None and id == None :
            return redirect(url_for('hello'))
        else:
            event = {}
            #query for getting event information based on name and id
            result = db.executeQuery(db.selectEventQueryD.format(str(id),name))
            if result:
                result = result[0]
                #get host information
                hostres = db.executeQuery(db.selectHostQuery.format(str(result[4])))
                host = "User Not Found" if hostres is None else hostres[0][0]
                schoolres = db.executeQuery(db.schoolInfoQuery.format(str(result[3])))
                if schoolres is None:
                    school = {'school_name':"Location Not Found"}
                else:
                    schoolres = schoolres[0]
                    fName = db.executeQuery(db.selectFName.format(result[2],result[3]))[0][0]
                    school = {'school_id': schoolres[0], 'school_name':schoolres[1], 'school_address':schoolres[2] + ' in facility ' + fName}
                    event = {'id': result[0], 'name': result[1], 'school': school,
                    'host': host, 'time_start': result[5], 'description': result[11],
                    'event_price': result[10], 'pictureUrl': 'https://asimshrestha2.github.io/imgs/content/environment.png' }
                    pictureURLres = db.executeQuery(db.selectImageQuery.format(result[0]))
                    if pictureURLres is not None:
                        event['pictureUrl'] = pictureURLres[0][0]
                    #since these variables are needed for payment, make sure donation is only on this page so people won't somehow donate to another event
                    session['eid'] = result[0]
                    session['ename'] = result[1]
                    session['state'] = schoolres[3]
                return render_template('eventpage.html', event=event, eventname = name, host = host, key='pk_test_Wb0XXIL9w6ez0dqn0z4JLIg4')
            else:
                abort(404)

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
            result = result[0]
            session['userstate'] = result[12]
            session['username'] = username
            session['userType'] = result[5]
            return url_for('user', name = username)
        #else we have wrong password
        return "-1"
    else:
        if(session.get('username')):
            return redirect(url_for('hello'));
        return render_template('login.html')

#TODO: Change logout return
@application.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('userType', None)
    #session.pop('userInfo', None)
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
        state = checkInput(request.form['state'])
        isUserExist = db.executeQuery(db.chkUsernameQuery.format(username))
         #invariant: No username's can be the same
        if result is not None: #then we already have this username
            return "-2"
        row1 = db.executeQuery(db.registerQuery.format(name,email,phone_num,uzip,user_type,username,password,user_address,0,state))
        #create some session variables with data that will be used frequently
        if row1:
            # Returns if query somehow returns a row which it shouldnt because we are inserting
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

@application.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'POST':
        res = calendarf.getweekevents()
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
    searchword = request.args.get('q', '')
    query = "select * from event where event_name like '%" + searchword + "%';"
    results = db.executeQuery(query)
    return(render_template('search.html', results = results))

@application.route('/eventsearch', methods=['GET', 'POST'])
def eventsearch():
    if request.method == 'POST':
        events = []
        sd = request.form['start-date']
        ed = request.form['end-date']
        searchword = request.form['search']
        events = eventmanager.geteventsearch(sd, ed, searchword)
        response = application.response_class(
            response=json.dumps(events),
            status=200,
            mimetype='application/json'
        )
        return "-1" if not events else response
    else:
        if session.get('userType') == 'Admin':
                return render_template('searchevents.html')
        else:
            abort(404)

#TODO: Add more to create event
@application.route('/createevent', methods=['GET', 'POST'])
def createevent():
    if request.method == 'POST':
        date_f = str(request.form['date'])
        stime_f = str(request.form['shour'])+":"+str(request.form['sminute'])+":00"
        etime_f = str(int(request.form['ehour']))+":"+str(request.form['eminute'])+":00"

        hostres = db.executeQuery("select user_id from user where username='" + str(session.get('username')) + "';")
        host_id = "User Not Found" if hostres is None else hostres[0][0]

        event = {'event_name': request.form['eventname'], 'facility_id': request.form['facility_id'],
        'school_id': request.form['school_id'], 'host_id': host_id,
        'time_start': stime_f, 'time_end': etime_f,
        'date': date_f, 'size': 123,
        'event_type': request.form['event_type'], 'event_price': 20.00,
        'description': request.form['description'],'pictureUrl':request.form['photolink']}
        print(event)
        db.executeQuery("""
            insert into event(event_name, facility_id, school_id, host_id, time_start, time_end, date, size, event_type, event_price, description, event_url)
            values('{event_name}', '{facility_id}', '{school_id}', '{host_id}', '{time_start}', '{time_end}', '{date}', '{size}', '{event_type}', '{event_price}', '{description}','{pictureUrl}');
        """.format(**event))
        eventres = db.executeQuery("""select event_id, event_name from event
            where event_name = '{event_name}' and school_id = '{school_id}' and host_id = '{host_id}';
        """.format(**event))
        print(eventres)
        eventinfo = {}
        if eventres is None:
            eventinfo = None
        else:
            eventinfo = {'eid': eventres[0][0], 'ename': eventres[0][1]}
        print(eventinfo)
        if eventres:
            return url_for('event', id=eventinfo['eid'], name=eventinfo['ename'])
        return "-1"
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

# TODO: Handle the Money API

@application.route('/test')
def test():
    #if you want emails to be set to the ones you logged in with, uncomment the comments below
    #emailRes = db.executeQuery(db.getUserEmailQuery.format(session['username']))[0][0]
    stripeM.balance()
    return render_template('test.html', key='pk_test_Wb0XXIL9w6ez0dqn0z4JLIg4')#, email = emailRes)

@application.route('/charge', methods=['POST'])
def charge():
# Amount in cents
    stripeM.errhandlingwrapper(stripeM.charge())
    return render_template('charge.html')

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


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
