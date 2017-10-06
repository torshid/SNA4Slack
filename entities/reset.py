from flask import redirect, url_for

from common import *

import os

page = Blueprint(__name__)


@page.route('/reset')
def main():
    for name in os.listdir("entities"):
        if name.endswith(".py"):
            modname = name[:-3]
            module = __import__('entities.' + modname, fromlist = ['reset'])
            if hasattr(module, 'reset'):
                func = getattr(module, 'reset')
                if callable(func):
                    func()
    return redirect(url_for('entities.home.main'))


@page.route('/reset/<string:modname>')
def specific(modname):
    module = __import__('entities.' + modname, fromlist = ['reset'])
    if hasattr(module, 'reset'):
        func = getattr(module, 'reset')
        if callable(func):
            func()
    return redirect(url_for('entities.home.main'))


@page.route('/pull')
def pull():
    os.system('git pull origin master')
    return redirect(url_for('entities.home.main'))