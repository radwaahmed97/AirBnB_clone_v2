#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask

applicaiton = FLask(__name__)
"""flask application instance"""
application.url_map.strict_slashes = False


@application.route('/')
def index():
    """The home page"""
    return 'Hello HBNB!'


if __name__ == '__main__':
    application.run(host='0.0.0.0', port='5000')
