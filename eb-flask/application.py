from flask import Flask, session, render_template, redirect, url_for, escape, request, json
import os
import sys
import MySQLdb
import dbconnection
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
    user = {
        'name': name,
        'title': 'User',
        'rating': [{'title': "Support", 'rating': 9},
            {'title': "Apple", 'rating': 5},
            {'title': "Potato", 'rating': 8}],
        'pictureUrl': 'https://asimshrestha2.github.io/portfoliov2/imgs/Asim_Ymir.png',
        'events': [{'title': "Dance", 'discription': "This is a discription for the dance event that is going on",
            'pictureUrl': 'http://orig13.deviantart.net/ac10/f/2015/100/c/4/render_4_edited_by_asimshrestha2-d8p8rbi.png'},
            {'title': "Dance No. 2", 'discription': "This is a discription for the dance event 2 that is going on",
            'pictureUrl': 'http://orig13.deviantart.net/ac10/f/2015/100/c/4/render_4_edited_by_asimshrestha2-d8p8rbi.png'},
            {'title': "Dance No. 3", 'discription': "This is a discription for the dance event 3 that is going on",
            'pictureUrl': 'http://orig13.deviantart.net/ac10/f/2015/100/c/4/render_4_edited_by_asimshrestha2-d8p8rbi.png'}]
    }
    return render_template('profile.html', user=user)

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
            'discription': "This is the description from Python",
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
        print(db.loginQuery.format(username,password), file=sys.stderr)
        row1 = db.executeQuery(db.loginQuery.format(username, password))
        #if sucessful will continue on, else will throw error inside executeQuery
        #just some debug stuff for now
        if row1 is not None:
            print('%s' % str(row1[0][1]), file=sys.stderr)
            #create some session variables with data that will be used frequently
            session['Username'] = row1[6]
            session['UserType'] = row1[5]
            return redirect(url_for('hello'))
    return render_template('login.html')

#TODO: Change logout return
@application.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('hello'))

@application.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('hello'))
    else:
        return render_template('signup.html')

# set the secret key.  keep this really secret:
#TODO: Change secret_key
application.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@application.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if request.method == 'POST':
        print(request.form['date'])
        res = [{'date':'8/4/2016', 'events':[{'title': "Event No. 1", 'discription': "This is something"},
            {'title': "Event No. 2", 'discription': "This is something"},
            {'title': "Event No. 3", 'discription': "This is something"}]},
            {'date':'9/4/2016', 'events':[{'title': "Event No. 1", 'discription': "This is something"},
            {'title': "Event No. 2", 'discription': "This is something"},
            {'title': "Event No. 3", 'discription': "This is something"}]},
            {'date':'10/4/2016', 'events':[]},
            {'date':'11/4/2016', 'events':[{'title': "Event No. 1", 'discription': "This is something"},
            {'title': "Event No. 2", 'discription': "This is something"}]}]
        response = application.response_class(
            response=json.dumps(res),
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        return render_template('calendar.html')

#TODO: Add more to create event
@application.route('/createevent')
def createevent():
    return(render_template('createevent.html'))

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
    
    
# TODO: Need database class that handles all the database commands and connection
# TODO: Need a social media api handling class
# TODO: Handle the Money API

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
