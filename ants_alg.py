import random
from graph import *

best_path = []
best_length = 0

start_node=1
target=1
Q=10.0
p=0.2
al = 0.1
be = 0.2
count_ants = 5
ants = []

graph = new_graph()

def choice(p):
	p = list(p)
	for i in range(len(p) - 1):
		p[i+1] = p[i+1] + p[i]
 
	rnd = random.random()
	for index, value in enumerate(p):
		if rnd <= value:
			return index
 

def reset_ant(ant, ants, init_pos):
        print(ant)	
	ind_ant = ants.index(ant)
	del ants[ind_ant]
	ants.append({'n': ant['n'], 'pos': init_pos, 'way':[init_pos]})

def init_ants(init_pos, count_ants):
	global ants
	
	for i in range(count_ants):
		ants.append({'n': i, 'pos': init_pos, 'way':[init_pos]})

def len_path(graph, node1, node2):
        print(node1)
        print(node2)
	return graph[node1][node2][0]
	

def len_way(graph, way):
	sum_length = 0
	for i in range(len(way) - 1):
		if i + 1 < len(way):
			sum_length = sum_length + len_path(graph, way[i], way[i + 1])
	return sum_length		

def add_pher(graph, node1, node2):
	params = graph[node1][node2]
	graph[node1][node2] = (params[0], Q / params[0])

def evaporate_pher(graph):
	global p
	for nodei in graph:
		links = graph[nodei]
		for node_link in links:
			params = links[node_link]
			new_pher_val = params[1] * (1 - p)
			links[node_link] = (params[0], new_pher_val)

def do_step(graph, ant, target):
	global best_path, best_length, start_node

	available_paths = graph[ant['pos']]

	for path in ant['way']:
		if path in available_paths:
			available_paths.pop(path)
	
	if available_paths == {}:
		reset_ant(ant['n'], ants, start_node)
		return
	
	ps = []
	all_paths = 0
	for path in available_paths:
		params = available_paths[path]
		all_paths = all_paths + pow(params[1], al) * pow(1.0/params[0], be)

	for path in available_paths:
		params = available_paths[path]
		p = pow(params[1], al) * pow(1.0/params[0], be) / all_paths 
		ps.append(p)

	paths = available_paths.keys()
	chosen_path = paths[choice(tuple(ps)) + 0]
	
	ant['way'].append(chosen_path)
	ant['pos'] = chosen_path

	if chosen_path == target:
		if len_way(graph, ant['way']) < best_length:
			best_path = ant['way']
			best_length = len_way(graph, ant['way'])
		reset_ant(ant, ants, start_node)

	last_2paths = ant['way'][-2:]
	add_pher(graph, last_2paths[0], last_2paths[1])

def max_length(graph):
	max_val = 0
	for i in graph:
		for j in graph[i]:
			params = graph[i][j]
			max_val = max_val + params[0]
	return max_val

def set_start(start):
	global start_node
	start_node = start

def set_target(target_pos):
	global target
	target = target_pos

def do_ants_alg(ants_count, steps, graph, start_pos, target):
	global ants, best_length, best_path
	init_ants(start_pos, ants_count)
	set_start(start_pos)
	set_target(target)
	best_length = max_length(graph)
	for step in range(steps):
		for ant in ants:
			do_step(graph, ant, target)
		evaporate_pher(graph)
	return (best_path, best_length)

def set_evaporate(value):
	global p
	p = value

def set_al_be_params(a, b):
	global al, be
	al = a
	be = b

def set_ant_pheromone(val):
	global Q
	Q = val

###################################################################################
