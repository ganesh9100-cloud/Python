from flask import Flask, render_template, redirect, make_response, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_URI
from forms import LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "1234 This is a secret key 7890"

db = SQLAlchemy(app)

# @app.route('/admin', methods = ['GET', 'POST'])
# def admin():
#     # return "Admin Login Form"
#     # In case of not requiring a CSRF token, it can be disabled while creating the object of LoginForm class. And, it does not require any secret key.
#     # adminlogin = LoginForm(csrf_enable=False)
#     adminlogin = LoginForm()
#     return render_template('admin.html', login_form = adminlogin)

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    admins = {'Mark' : 'Mark@123', 'Ben' : 'Ben@123', 'Sash' : 'Sash@123'}
    adminlogin = LoginForm()
    message = ""
    if adminlogin.validate_on_submit():
        admin_name = adminlogin.login_name.data
        admin_pass = adminlogin.login_password.data
        if admin_name in admins:
            if admin_pass == admins[admin_name]:
                session['admin'] = admin_name
                response_object = make_response(render_template('events.html'))
                response_object.set_cookie('admin', admin_name)
                # return response_object
                # return render_template('events.html')  #this will render the page but we will stay on the same url at the browser.
                # return redirect('/tasks')             #this will redirect to particular route and we need to give route url
                return redirect(url_for('get_tasks'))   #this will redirect to particular function and we need to give function name
            else:
                message = "Incorrect password!"
        else:
            # return redirect(url_for('get_tasks'))
            message = "Oops! You are not authorised as admin!"
            abort(401, description = "Please login as admin!")
    return render_template('admin.html', message = message, login_form = adminlogin)

@app.route('/add-events')   #we can use mutilple decorators for a single function so that we can access the function with multiple urls.
@app.route('/add-event')
def add_event():
    #add event logic goes here ...
    if 'admin' in session:
        return render_template('add_event.html')
    return redirect('/events')

@app.errorhandler(401)
@app.errorhandler(404)
def page_not_found(error):
    return error
#Such scenarios can be handled by the errorhandler() decorator. This method takes the error code as its argument, 
#since, it cannot be mapped to any specific URL. The object of the corresponding error code is passed to the view function.

from routes import *

if __name__ == '__main__':
    app.run(debug=True)
    

# Create Session: Create a new key-value pair in dictionary as, session['key'] = 'value'
# Access Session: Access the corresponding key from the session dictionary as, session['key']
# Delete Session: Remove the key from the session dictionary as, session.pop('key')
