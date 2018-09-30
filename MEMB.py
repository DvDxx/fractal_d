import networkx as nx
import random
from copy import deepcopy

def MEMB(G, rb, cycle=0):
    """
	It returns a dictionary with {box_id:subgraph_generated_by_the_nodes_in_this_box}
	The box_id is the center of the box.
	cycle: Ignore this parameter. Use the default cycle=0.
	"""
    adj = G.adj
    number_of_nodes = G.number_of_nodes()
    # print number_of_nodes
    covered_nodes = set()
    center_nodes = set()
    non_center_nodes = list(G.nodes())
    center_node_found = 0
    boxes = {}  # this will be "box_id:[nodes in box]"
    central_distance_of_node = {}  # "node:central_distance"
    node_box_id = {}  # "node:box_id"
    nodes_sorted_by_central_distance = {}  # Dict with {central_distance:[nodes]}
    excluded_mass_of_non_centers_rb = {}  # This contains [(node:excluded_mass)] for rb
    excluded_mass_of_non_centers_rb2 = {}  # This contains [(node:excluded_mass)] for rb+1
    rb2 = rb + 1
    for node in non_center_nodes:
        # if node in [5000,10000,20000,30000]: print "node", node
        level = 0  # the current level
        nextlevel = {node: 1}  # list of nodes to check at next level
        paths_rb = None
        paths_rb2 = {node: [node]}  # paths dictionary  (paths to key from source)
        while nextlevel:
            paths_rb = deepcopy(paths_rb2)
            thislevel = nextlevel
            nextlevel = {}
            for v in thislevel:
                for w in G.neighbors(v):
                    if w not in paths_rb2:
                        paths_rb2[w] = paths_rb2[v] + [w]
                        nextlevel[w] = 1
            level = level + 1
            if rb2 <= level:
                break
        excluded_mass_of_node = len(paths_rb2)
        try:
            excluded_mass_of_non_centers_rb2[excluded_mass_of_node].append(node)
        except KeyError:
            excluded_mass_of_non_centers_rb2[excluded_mass_of_node] = [node]
        excluded_mass_of_node = len(paths_rb)
        try:
            excluded_mass_of_non_centers_rb[excluded_mass_of_node].append(node)
        except KeyError:
            excluded_mass_of_non_centers_rb[excluded_mass_of_node] = [node]
    maximum_excluded_mass = 0
    nodes_with_maximum_excluded_mass = []
    new_covered_nodes = {}
    center_node_and_mass = []
    cycle_index = 0
    while len(covered_nodes) < number_of_nodes:
        # print len(covered_nodes),number_of_nodes
        cycle_index += 1
        if cycle_index == cycle:
            rb2 = rb + 1
            cycle_index = 0
        else:
            rb2 = rb
        while 1:
            if rb2 == rb + 1:
                # t1=time.time()
                while 1:
                    maximum_key = max(excluded_mass_of_non_centers_rb2.keys())
                    node = random.choice(excluded_mass_of_non_centers_rb2[maximum_key])
                    if node in center_nodes:
                        excluded_mass_of_non_centers_rb2[maximum_key].remove(node)
                        if not excluded_mass_of_non_centers_rb2[maximum_key]: del excluded_mass_of_non_centers_rb2[
                            maximum_key]
                    else:
                        break
                nodes_visited = {}
                bfs = nx.single_source_shortest_path(G, node, cutoff=rb2)
                for i in bfs:
                    nodes_visited[i] = len(bfs[i]) - 1
                excluded_mass_of_node = len(set(nodes_visited.keys()).difference(covered_nodes))
                if excluded_mass_of_node == maximum_key:
                    center_node_and_mass = (node, maximum_key)
                    excluded_mass_of_non_centers_rb2[maximum_key].remove(node)
                    if not excluded_mass_of_non_centers_rb2[maximum_key]: del excluded_mass_of_non_centers_rb2[
                        maximum_key]
                    new_covered_nodes = nodes_visited
                    break
                else:
                    excluded_mass_of_non_centers_rb2[maximum_key].remove(node)
                    if not excluded_mass_of_non_centers_rb2[maximum_key]: del excluded_mass_of_non_centers_rb2[
                        maximum_key]
                    try:
                        excluded_mass_of_non_centers_rb2[excluded_mass_of_node].append(node)
                    except KeyError:
                        excluded_mass_of_non_centers_rb2[excluded_mass_of_node] = [node]
            # print "time", time.time()-t1
            else:
                # t1=time.time()
                while 1:
                    maximum_key = max(excluded_mass_of_non_centers_rb.keys())
                    node = random.choice(excluded_mass_of_non_centers_rb[maximum_key])
                    if node in center_nodes:
                        excluded_mass_of_non_centers_rb[maximum_key].remove(node)
                        if not excluded_mass_of_non_centers_rb[maximum_key]: del excluded_mass_of_non_centers_rb[
                            maximum_key]
                    else:
                        break
                nodes_visited = {}
                bfs = nx.single_source_shortest_path(G, node, cutoff=rb)
                for i in bfs:
                    nodes_visited[i] = len(bfs[i]) - 1
                excluded_mass_of_node = len(set(nodes_visited.keys()).difference(covered_nodes))
                if excluded_mass_of_node == maximum_key:
                    center_node_and_mass = (node, maximum_key)
                    excluded_mass_of_non_centers_rb[maximum_key].remove(node)
                    if not excluded_mass_of_non_centers_rb[maximum_key]: del excluded_mass_of_non_centers_rb[
                        maximum_key]
                    new_covered_nodes = nodes_visited
                    break
                else:
                    excluded_mass_of_non_centers_rb[maximum_key].remove(node)
                    if not excluded_mass_of_non_centers_rb[maximum_key]: del excluded_mass_of_non_centers_rb[
                        maximum_key]
                    try:
                        excluded_mass_of_non_centers_rb[excluded_mass_of_node].append(node)
                    except KeyError:
                        excluded_mass_of_non_centers_rb[excluded_mass_of_node] = [node]
            # print "time", time.time()-t1

        center_node_found = center_node_and_mass[0]
        boxes[center_node_found] = [center_node_found]
        node_box_id[center_node_found] = center_node_found
        non_center_nodes.remove(center_node_found)
        center_nodes.add(center_node_found)

        covered_nodes = covered_nodes.union(set(new_covered_nodes.keys()))
        # print len(covered_nodes)
        for i in new_covered_nodes:

            try:
                if central_distance_of_node[i] > new_covered_nodes[i]:
                    nodes_sorted_by_central_distance[central_distance_of_node[i]].remove(i)
                    if not nodes_sorted_by_central_distance[central_distance_of_node[i]]:
                        del nodes_sorted_by_central_distance[central_distance_of_node[i]]
                    try:
                        nodes_sorted_by_central_distance[new_covered_nodes[i]].append(i)
                    except KeyError:
                        nodes_sorted_by_central_distance[new_covered_nodes[i]] = [i]
                    central_distance_of_node[i] = new_covered_nodes[i]
            except KeyError:
                central_distance_of_node[i] = new_covered_nodes[i]
                try:
                    nodes_sorted_by_central_distance[new_covered_nodes[i]].append(i)
                except:
                    nodes_sorted_by_central_distance[new_covered_nodes[i]] = [i]

    max_distance = max(nodes_sorted_by_central_distance.keys())
    for i in range(1, max_distance + 1):
        for j in nodes_sorted_by_central_distance[i]:
            targets = list(set(adj[j].keys()).intersection(set(nodes_sorted_by_central_distance[i - 1])))
            node_box_id[j] = node_box_id[random.choice(targets)]
            boxes[node_box_id[j]].append(j)
    boxes_subgraphs = {}  # a dictionary with {box_id:subgraph_generated_by_the_nodes_in_this_box}
    # print boxes
    for i in boxes:
        boxes_subgraphs[i] = nx.subgraph(G, boxes[i])
    return len(boxes_subgraphs)