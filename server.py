from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.script import Manager
from datetime import datetime
from flask.ext.moment import Moment

app = Flask(__name__)
Bootstrap(app)
manager = Manager(app)
moment = Moment(app)


@app.route('/')
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('index.html', name=name, current_time=datetime.utcnow())


if __name__ == '__main__':
    manager.run()
