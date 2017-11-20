from common import *

page = Blueprint(__name__)


@page.route('/graphs/eigen', methods=['POST', 'GET'])
def main():
    return call_graph('eigen')


@page.route('/graphs/eigen.json', methods=['POST'])
def json():
    return get_json('eigen')
