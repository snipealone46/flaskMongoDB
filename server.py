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
            return True
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
        inputinfo = LoginDB(login.ID.data, login.password.data)
        if inputinfo.checkexist():
            session['user'] = login.ID.data
        else:
            flash('The username does not exist!')
        return redirect(url_for('forum'))
    return render_template('index.html', login=login, user=session.get('user'))


if __name__ == '__main__':
    manager.run()
