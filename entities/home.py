from flask import render_template, request, redirect, url_for

from common import *

page = Blueprint(__name__)


@page.route('/', methods=['POST', 'GET'])
def main():
    if request.method == 'POST':
        return redirect(url_for('entities.graph_' + request.form['metric'] + '.main'
                                ), code=307)
    return render_template('home.html')