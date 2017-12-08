import json
import requests
import networkx as nx

class Node:
    def __init__(self, id, label, role, root):
        self.id = id
        self.label = label
        self.role = role
        self.root = root
        self.degree = 0
        self.eigenvalue = 1
        self.radius = 1

class Edge:
    def __init__(self, source, target, label):
        self.source = source
        self.target = target
        self.label = label
        self.weight = 1

class User:
    def __init__(self, id, slack_id, name, role = 'user', root = False):
        self.id = id
        self.slack_id = slack_id
        self.name = name
        self.role = role
        self.root = root

class Channel:
    def __init__(self, id, slack_id, name, members, role = 'channel', root = True):
        self.id = id
        self.slack_id = id
        self.name = name
        self.members = members
        self.role = role
        self.root = root

    def get_users(self, users, nodes, edges, usernames):
        for member in self.members:
            if not member in users:
                users[member] = User(len(users), member, usernames[member])

    def get_nodes(self, users, nodes, edges, usernames):
        #nodes[self.slack_id] = Node(len(nodes), self.name, self.role, self.root)

        for member in self.members:
            if not member in nodes:
                nodes[member] = Node(len(nodes), users[member].name, users[member].role, users[member].root)

    def get_edges(self, users, nodes, edges, usernames):
        size = len(self.members)

        #for index in range(0, size):
        #    member = self.members[index]
        #    if not (member, self.slack_id) in edges and not (self.slack_id, member) in edges:
        #        edges[(member, self.slack_id)] = Edge(nodes[member].id, nodes[self.slack_id].id, 'join')
        #        nodes[member].degree += 1
        #        nodes[self.slack_id].degree += 1
        #    # one person can only be in a channel once do need to increment the weight

        for index1 in range(0, size - 1):
            for index2 in range(index1 + 1, size):
                member1 = self.members[index1]
                member2 = self.members[index2]

                if not (member1, member2) in edges and not (member2, member1) in edges:
                    edges[(member1, member2)] = Edge(nodes[member1].id, nodes[member2].id, 'contact')
                    nodes[member1].degree += 1
                    nodes[member2].degree += 1
                elif (member1, member2) in edges:
                    edges[(member1, member2)].weight += 1
                elif (member2, member1) in edges:
                    edges[(member2, member1)].weight += 1

class Team:
    def __init__(self, id, slack_id, name, role = 'team', root = True):
        self.id = id
        self.slack_id = slack_id
        self.name = name
        self.role = role
        self.root = root

## degree: number of links
## often used as measure of a node's degree of connectedness and
## hence also influence and/or popularity
## useful in assessing which nodes are central with respect to
## spreading information and influencing others in their
## immediate 'neighborhood'

## path: a path between two nodes is any sequence
## of non-repeating nodes that connects the two nodes
## shortest path is the distance between nodes
## shorter paths are desirable when speed of communication or exchange is desired

## eigen vector: a nodes's eigen vector is proportional
## to the sum of the eigenvector of all nodes directly connected to it
## in other words, a node with a high eigen vector is connected to
## other nodes with high eigen vector
## similar to Google ranks web pages, links from highly linked-to pages count more
## useful in determining who is connected to the most connected nodes

class MyGraph:
    def __init__(self, nodes, edges, threshold, sna_metric):
        self.nodes = []
        self.edges = []
        self.adj = []
        self.degrees = []
        self.eigenvalues = []
        self.weights = []
        self.threshold = int(threshold)
        self.sna_metric = sna_metric

        #nodes -> string(node name) to Node object
        #edges -> string(node name), string(node name) to Edge object

        #self.nodes -> index to dict
        #self.edges -> index to dict
        #self.adj -> 2d int matrix
        #self.degrees -> index to int
        #self.eigenvalues -> index to int
        #self.weights -> index to int

        for node in nodes:
            if nodes[node].role == 'channel' or nodes[node].role == 'team':
                self.nodes.append({'id': nodes[node].id, 'caption': nodes[node].label, 'role': nodes[node].role, 'root': nodes[node].root, 'radius': nodes[node].radius})
            elif nodes[node].role == 'user':
                if nodes[node].degree > self.threshold:
                    self.nodes.append({'id': nodes[node].id, 'caption': nodes[node].label, 'role': nodes[node].role, 'root': nodes[node].root, 'radius': nodes[node].radius})

        for (node1, node2) in edges:
            self.edges.append({'source': edges[(node1, node2)].source, 'target': edges[(node1, node2)].target, 'caption': edges[(node1, node2)].label + ' in {} channels'.format(edges[(node1, node2)].weight), 'width': edges[(node1, node2)].weight})
            self.weights.append(edges[(node1, node2)].weight)


        # look  if networkx has eigen vector, path length and degree
        for node1 in nodes:
            node1_adj_matrix = []
            for node2 in nodes:
                if (node1, node2) in edges:
                    node1_adj_matrix.append(1)
                else:
                    node1_adj_matrix.append(0)
            self.adj.append(node1_adj_matrix)

        for i in range(0, 10):# 10 -> iteration number, epsilon can be used as well
            for node1 in nodes:
                for node2 in nodes:#transpoze -> self.adj[nodes[node2].id][nodes[node1].id]
                    nodes[node1].eigenvalue += self.adj[nodes[node1].id][nodes[node2].id] / nodes[node1].degree

        for node in nodes:
            self.degrees.append(nodes[node].degree)
            self.eigenvalues.append(nodes[node].eigenvalue)

def get_usernames(url):
    usernames = {}

    response = requests.get(url)
    r = response.json()
    if r['ok'] == True:
        for member in r['members']:
            usernames[member['id']] = member['name']
    else:
        return (False, {})

    return (True, usernames)

def get_channels(url):
    channels = []

    response = requests.get(url)
    r = response.json()
    if r['ok'] == True:
        channel_index = 0
        for channel_info in r['channels']:
            channel_id = len(channels)
            channel_slack_id = channel_info['id']
            channel_name = channel_info['name']
            channel_members = channel_info['members']

            #actual channels
            channels.append(Channel(channel_id, channel_slack_id, channel_name, channel_members))
    else:
        return (False, {})

    return (True, channels)

def get_team(url):
    team = None
    response = requests.get(url)
    r = response.json()
    if r['ok'] == True:
        team = Team(0, r['team']['id'], r['team']['name'])
    else:
        return (False, None)

    return (True, team)

def do_it(api_key, threshold = '0', sna_metric = "Degree"):
    users = {}
    nodes = {}
    edges = {}

    ret, team_info = get_team('https://slack.com/api/team.info?token={}&pretty=1'.format(api_key))
    #nodes[team_info.slack_id] = Node(team_info.id, team_info.name, team_info.role, team_info.root)

    ret, channels = get_channels('https://slack.com/api/channels.list?token={}&pretty=1'.format(api_key))
    ret, usernames = get_usernames('https://slack.com/api/users.list?token={}&pretty=1'.format(api_key))
    
    for channel in channels:
        print(channel.name)
        if channel.name != 'general':
            channel.get_users(users, nodes, edges, usernames)
            channel.get_nodes(users, nodes, edges, usernames)

            #edges[(channel.slack_id, team_info.slack_id)] = Edge(nodes[channel.slack_id].id, nodes[team_info.slack_id].id, 'in')
            #nodes[channel.slack_id].degree += 1
            #nodes[team_info.slack_id].degree += 1

            channel.get_edges(users, nodes, edges, usernames)

    graph_info = MyGraph(nodes, edges, threshold, sna_metric)

    # change information taken from slack to networkx graph
    # modify data structure
    G = nx.Graph()
    elist = []
    sna_data = {}

    # when adding weight use G.add_weighted_edges_from(elist)
    # and make elist[("a","b", 2.0)]
    for edge in graph_info.edges:
        elist.append((edge["source"], edge["target"]))
    G.add_edges_from(elist)

    if sna_metric == "Degree":
        sna_data = nx.degree_centrality(G)
    elif sna_metric == "Eigenvector":
        sna_data = nx.eigenvector_centrality(G)
    elif sna_metric == "Shortest Path":
        sna_data = nx.betweenness_centrality(G)
    for node in graph_info.nodes:
        node["radius"] = sna_data[node["id"]]

    print(sna_metric, sna_data)
    min_radius = min(graph_info.nodes, key = lambda node: node['radius'])['radius']
    max_radius = max(graph_info.nodes, key = lambda node: node['radius'])['radius']
    print(min_radius, max_radius)

    # if min == max dont do this part
    #scaling
    if min_radius != max_radius:
        for node in graph_info.nodes:
            zero_one = (node["radius"] - min_radius) / (max_radius - min_radius)
            node["radius"] = int(30 * zero_one + 10)
    else:
        for node in graph_info.nodes:
            node["radius"] = 40

    min_width = min(graph_info.edges, key = lambda edge: edge['width'])['width']
    max_width = max(graph_info.edges, key = lambda edge: edge['width'])['width']
    print(min_width, max_width)

    if min_width != max_width:
        for edge in graph_info.edges:
            zero_one = (edge["width"] - min_width) / (max_width - min_width)
            edge["width"] = 2 * zero_one + 2
            print(edge['width'])
    else:
        for edge in graph_info.edges:
            edge["width"] = 4

    json_data = json.dumps({'nodes': graph_info.nodes, 'edges': graph_info.edges, 'weights': graph_info.weights, 'sna_metrics': sna_data}, indent = 4, sort_keys = True)
    return json_data
