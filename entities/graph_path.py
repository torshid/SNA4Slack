from common import *

page = Blueprint(__name__)


@page.route('/graphs/path', methods=['POST', 'GET'])
def main():
    return call_graph('path')


@page.route('/graphs/path.json', methods=['POST'])
def json():
    return get_json('path')
