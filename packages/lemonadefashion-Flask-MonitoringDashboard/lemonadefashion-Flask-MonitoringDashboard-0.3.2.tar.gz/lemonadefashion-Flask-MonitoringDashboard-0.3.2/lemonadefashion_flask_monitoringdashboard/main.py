"""This file can be executed for developing purposes.
To run use:

>>> python main.py

Note: This is not used when the lemonadefashion_flask_monitoringdashboard
is attached to your flask application.
"""
import time
from random import random, randint

from flask import Flask, redirect, url_for

import lemonadefashion_flask_monitoringdashboard as dashboard

app = Flask(__name__)

dashboard.config.group_by = '2'

def on_the_minute():
    return int(random() * 100 // 10)

minute_schedule = {'second': 00}

def every_ten_seconds():
    return int(random() * 100 // 10)

every_ten_seconds_schedule = {'seconds': 10}
dashboard.config.init_from(config={
    'version': '3.2',
    'blueprint_name': 'monitoring',
    'scheme': 'http',
    'host': '127.0.0.1:5000',
    'link': 'monitoring',
    'monitor_level': 3,
    'outlier_detection_constant': 4,
    'sampling_period': 50,
    'enable_logging': False,
    'username': 'dev',
    'password': '8743862589bafbc7739824ba7c98343a',
    'security_token': '8743862589bafbc7739824ba7c98343a',
    'database_name': 'sqlite:///data.db',
    'table_prefix': 'fmd',
    'colors': {
        'main': '[0,97,255]',
        'static': '[255,153,0]'
    },
    'timezone': 'Asia/Beirut'
})
dashboard.config.inject_dependencies()
dashboard.add_graph("Every 10 Seconds", every_ten_seconds, "interval", **every_ten_seconds_schedule)
dashboard.add_graph("On Half Minute", on_the_minute, "cron", **minute_schedule)
dashboard.bind(app)

@app.route('/')
def to_dashboard():
    return redirect(url_for(dashboard.config.blueprint_name + '.login', _external=True,
                            _scheme=dashboard.config.scheme))


@app.route('/endpoint')
def endpoint():
    # if session_scope is imported at the top of the file, the database config won't take effect
    from lemonadefashion_flask_monitoringdashboard.database import session_scope

    with session_scope() as session:
        print(session.bind.dialect.name)

    print("Hello, world")
    return 'Ok'


@app.route('/endpoint2')
def endpoint2():
    time.sleep(0.5)
    return 'Ok', 400


@app.route('/endpoint3')
def endpoint3():
    time.sleep(0.1 if randint(0, 1) == 0 else 0.2)
    return 'Ok'


@app.route('/endpoint4')
def endpoint4():
    time.sleep(0.5)
    return 'Ok'


@app.route('/endpoint5')
def endpoint5():
    time.sleep(0.2)
    return 'Ok'


def my_func():
    # here should be something actually useful
    return 33.3


if __name__ == "__main__":
    app.run()
