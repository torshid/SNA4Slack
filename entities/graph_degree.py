from common import *

page = Blueprint(__name__)


@page.route('/graphs/degree', methods=['POST', 'GET'])
def main():
    return call_graph('degree')


@page.route('/graphs/degree.json', methods=['POST'])
def json():
    return get_json('degree')
