from werkzeug.exceptions import NotFound, Forbidden
from flask import Flask, app, render_template

from common import *
from config import *
import jinja

app = Flask(__name__)


# jinja-python functions
@app.context_processor
def processor():
    functions = {}
    for function in jinja.__dict__.values():
        if callable(function):
            functions[function.__name__] = function
    return functions

# dynamically load all entities + register blueprints
for name in os.listdir("entities"):
    if name.endswith(".py"):
        module = name[:-3]
        globals()[module] = __import__('entities.' + module, fromlist = ['page'])
        app.register_blueprint(getattr(globals()[module], 'page'))


@app.errorhandler(NotFound)
def error(e):
    return render_template('errors/' + str(e.code) + '.html'), e.code


@app.errorhandler(Forbidden)
def error(e):
    return render_template('errors/' + str(e.code) + '.html'), e.code


if __name__ == '__main__':
    app.secret_key = flaskkey
    app.run(host = '0.0.0.0', port = port, debug = debug)