def title():
    return "SNA4Slack"

def fileExists(name):
    import os
    if name[:1] == '/':
        name = name[1:]
    return os.path.isfile(os.path.dirname(os.path.abspath(__file__)) + '/' + name)


def menus():
    return {'Home': 'entities.home.main', 'Sample': 'entities.graph_sample.main'}
