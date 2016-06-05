from ants_alg import *

graph = new_graph()

add_node(1, graph)
add_node(2, graph)
add_node(3, graph)
add_node(4, graph)
add_node(5, graph)
add_node(6, graph)
add_node(7, graph)

add_nodes_link(graph, 1, 2, 2, 1)
add_nodes_link(graph, 1, 3, 4, 1)
add_nodes_link(graph, 1, 4, 3, 1)
add_nodes_link(graph, 2, 6, 8, 1)
add_nodes_link(graph, 3, 6, 3, 1)
add_nodes_link(graph, 4, 5, 2, 1)
add_nodes_link(graph, 5, 6, 1, 1)
add_nodes_link(graph, 4, 7, 1, 1)
add_nodes_link(graph, 6, 7, 1, 1)

set_ant_pheromone(10.0)
set_al_be_params(0.1, 0.2)
set_evaporate(0.2)
result = do_ants_alg(15, 2, graph, 1, 6)

print(result)

