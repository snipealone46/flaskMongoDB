from flask import Flask, flash, render_template, session, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from datetime import datetime
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import SubmitField, StringField, PasswordField, validators
from pymongo import MongoClient

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
client = MongoClient()
loginInfo = client.user.login

# moment = Moment(app)


class LoginDB(object):
    def __init__(self, username, password):
        self.login = loginInfo
        self.ID = username
        self.password = password

# checkexist(): if exist return true otherwise return false
    def checkexist(self):
        findmatch = self.login.find_one({"ID": "%s" % self.ID})
        if findmatch:
            return findmatch
        else:
            return False

    def passwordmatch(self):
        findmatch = self.checkexist()
        if findmatch:
            return findmatch['password'] == self.password
        else:
            return False

class ID(Form):
    ID = StringField('username', [validators.InputRequired(message='please enter your username')])


class LoginForm(ID):
    password = PasswordField('password')
    submit = SubmitField('Submit')


class RegisterForm(ID):
    emailValMessage = "Please enter a valid email address"
    userEmail = StringField('email', [validators.InputRequired(message=emailValMessage), validators.email(message=emailValMessage)])
    newPassword = PasswordField('New Password', [validators.InputRequired(), validators.EqualTo('confirm', message='Passwords must match')])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def forum():
    login = LoginForm()
    if login.validate_on_submit():
        session['user'] = login.ID.data
        session['password'] = login.password.data
        return redirect(url_for('logon'))
    elif 'user' in session:
        return render_template('login_true.html', user=session.get('user'))
    else:
        return render_template('login_false.html', login=login)


@app.route('/login', methods=['GET', 'POST'])
def logon():
    inputinfo = LoginDB(session.get('user'), session.get('password'))
    if not inputinfo.passwordmatch():
        session.pop('user', None)
        flash('The username or password does not match our record!')
    session.pop('password', None)
    return redirect(url_for('forum'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('forum'))


if __name__ == '__main__':
    manager.run()
