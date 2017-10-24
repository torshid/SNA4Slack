from flask import current_app, render_template
from common import *

page = Blueprint(__name__)


@page.route('/graphs/sample')
def main():
    return render_template('graph_sample.html')


@page.route('/graphs/sample.json')
def json():
    return current_app.send_static_file('sample_data2.json')