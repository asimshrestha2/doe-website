from flask import Flask, session, render_template, redirect, url_for, escape, request
import os
# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def hello():
    return render_template('index.html')

@application.route('/u/')
@application.route('/u/<name>')
def user(name=None):
    user = {
        'name': name,
        'title': 'User',
        'rating': [{'title': "Support", 'rating': 9},
            {'title': "Apple", 'rating': 5},
            {'title': "Potato", 'rating': 8}],
        'pictureUrl': 'https://asimshrestha2.github.io/portfoliov2/imgs/Asim_Ymir.png'
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
            'discription': "This is the discription from Python",
            'pictureUrl': 'https://asimshrestha2.github.io/imgs/content/environment.png'
        }
        return render_template('eventpage.html', event=event)

# Function for all the login user page
@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "POST Login"
    else:
        return render_template('login.html')

@application.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404

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

# TODO: Need database class that handles all the database commands and connection
# TODO: Need a social media api handling class
# TODO: Handle the Money API

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
