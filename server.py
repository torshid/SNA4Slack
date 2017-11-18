from werkzeug.exceptions import NotFound, Forbidden
from flask import Flask, app, render_template, request
from GraphInfo import do_it
from common import *
from config import *
import jinja

app = Flask(__name__)

@app.route("/")
def hello():
    json_data = do_it(api_key='API KEY HERE',threshold = 0,sna_metric = 'Degree')
    # json_data content is empty because of api key, but keys can be examined
    print(json_data)
    return render_template('home.html')

@app.route('/show', methods = ['POST', 'GET'])
def show():
    key = request.form['slack-key']
    threshold = request.form['threshold']
    sna_metric = request.form['sna-metric']
    
    print(do_it(key,threshold,sna_metric))
    # need to save the data
    # graph uses cached data have to make new file and send that filename to html
    # so we can se it in alchemy config
    return render_template('graph_sample.html')

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