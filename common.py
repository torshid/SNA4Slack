import flask

import GraphInfo


def Blueprint(name):  # new simple blueprint from given name
    return flask.Blueprint(name, name)


def valid_metric(metric):
    return metric == 'degree' or metric == 'path' or metric == 'eigen'


def call_graph(metric):
    if not valid_metric(metric):
        return flask.redirect(flask.url_for('entities.home.main'))
    if 'key' not in flask.request.form or 'threshold' not in flask.request.form:
        return flask.render_template('graph_' + metric + '.html',
                                     key='',
                                     threshold='')
    return flask.render_template('graph_' + metric + '.html',
                                 key=flask.request.form['key'],
                                 threshold=flask.request.form['threshold'])


def get_json(metric):
    if not valid_metric(metric):
        return flask.jsonify({'error': 'Invalid metric name.'})
    elif 'key' in flask.request.form and 'threshold' in flask.request.form:
        key = flask.request.form['key']
        threshold = flask.request.form['threshold']
        return GraphInfo.do_it(key, threshold, metric)
    return flask.jsonify({'error': 'Please specify key and threshold.'})
