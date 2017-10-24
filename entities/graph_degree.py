from flask import current_app, render_template, jsonify
from common import *

page = Blueprint(__name__)


@page.route('/graphs/degree')
def main():
    return render_template('graph_degree.html')


@page.route('/graphs/degree.json')
def json():
    return jsonify()