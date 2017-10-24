from flask import current_app, render_template, jsonify
from common import *

page = Blueprint(__name__)


@page.route('/graphs/path')
def main():
    return render_template('graph_path.html')


@page.route('/graphs/path.json')
def json():
    return jsonify()