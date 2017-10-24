from flask import current_app, render_template, jsonify
from common import *

page = Blueprint(__name__)


@page.route('/graphs/eigen')
def main():
    return render_template('graph_eigen.html')


@page.route('/graphs/eigen.json')
def json():
    return jsonify()