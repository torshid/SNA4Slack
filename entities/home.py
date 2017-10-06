from flask import render_template
from common import *

page = Blueprint(__name__)


@page.route('/')
def main():
    return render_template('home.html')