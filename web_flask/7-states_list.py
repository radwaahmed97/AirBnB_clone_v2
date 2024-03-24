#!/usr/bin/python3
"""script that starts a Flask web application"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_db(error):
    """ Remove current SQLAlchemy Session """
    storage.close()


@app.route('/states_list')
def states_list():
    """ displays HTML page with a list of states """
    allstates = list(storage.all(State).values())
    allstates.sort(key=lambda x: x.name)
    ctxt = {
        'states': all_states
    }
    return render_template('7-states_list.html', **ctxt)


if __name__ == "__main__":
    """ Main Function """
    app.run(host='0.0.0.0', port=5000)
