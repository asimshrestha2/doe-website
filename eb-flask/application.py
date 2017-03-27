from flask import Flask, session, render_template, redirect, url_for, escape, request

# EB looks for an 'application' callable by default.
application = Flask(__name__)

@application.route('/')
def hello():
    return render_template('index.html')

@application.route('/u/')
@application.route('/u/<name>')
def user(name=None):
    return render_template('profile.html', name=name)

@application.route('/e/')
@application.route('/e/<name>')
def event(name=None):
    if name == None:
        return redirect(url_for('hello'))
    else:
        return render_template('eventpage.html', name=name)

@application.errorhandler(404)
def page_not_found(error):
    return render_template('index.html'), 404

# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
