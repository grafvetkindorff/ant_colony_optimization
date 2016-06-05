#!/usr/bin/python2

########## nodes in graph (vertexes)
nodes = []

########## create list of links between nodes
def new_graph():
    return {}

######### clean the graph
def clean_graph(graph):
    global nodes
    nodes = []
    graph = {}
    return graph

########## add node in graph (and nodes list)
def add_node(node, graph):
    
    global nodes
    
    if not node in nodes:
        nodes.append(node)
        graph[node] = {}
    
    return graph

######### delete node from graph
def rm_node(node, graph):

    global nodes
    if node not in graph:
        return 
    graph.pop(node)

    for link in graph:
        if graph[link].has_key(node):
            graph[link].pop(node)

    nodes.pop(nodes.index(node))

######### add link between a, b
def add_nodes_link(graph, a, b, weight, param):
    
    graph[a][b] = (weight, param)
    graph[b][a] = (weight, param)

###################################################################################
