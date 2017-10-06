import flask

def Blueprint(name):  # new simple blueprint from given name
    return flask.Blueprint(name, name)