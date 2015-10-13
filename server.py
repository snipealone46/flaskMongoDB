from flask import Flask, render_template, session, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from datetime import datetime
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
manager = Manager(app)
moment = Moment(app)


class NameForm(Form):
    name = StringField('What is your name?', [InputRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        # session['name'] = sth => will save sth in client side and name it as variable 'name'
        return redirect(url_for('index'))
        # url_for('index') will return the url for 'def index()'
    # -------------------------example below----------------------------
    #         >>> app = Flask(__name__)
    #         >>> @app.route('/')
    #              ... def index(): pass
    #              ...
    #         >>> @app.route('/login')
    #              ... def login(): pass
    #              ...
    #         >>> @app.route('/user/<username>')
    #              ... def profile(username): pass
    #              ...
    #         >>> with app.test_request_context():
    #              ...  print url_for('index')
    #              ...  print url_for('login')
    #              ...  print url_for('login', next='/')
    #              ...  print url_for('profile', username='John Doe')
    #              ...
    #         /
    #         /login
    #         /login?next=/
    #         /user/John%20Doe
    # -----------------------------------------------------------------
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())
# session.get('name') will fetch the name variable in client side


if __name__ == '__main__':
    manager.run()
