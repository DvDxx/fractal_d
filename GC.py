import networkx as nx
import itertools
import random
def GC(G, lb, shortest_path):
    node_list = list(G.nodes())
    DualG = nx.Graph()
    DualG_adj = {}
    for i in node_list:
        DualG_adj[i] = set()
        for j in node_list:
            try:
                if (nx.shortest_path_length(G,i,j) >= lb):
                    DualG_adj[i].add(j)
                    DualG.add_edge(i, j)
            except Exception:
                pass
    #node_list = sorted(DualG, key=DualG.degree, reverse=True)
    node_list = random.shuffle(node_list)
    colors = {}
    for u in node_list:
        # Set to keep track of colors of neighbours
        neighbour_colors = {colors[v] for v in DualG[u] if v in colors}
        # Find the first unused color.
        for color in itertools.count():
            if color not in neighbour_colors:
                colors[u] = color
                break
        # Assign the new color to the current node.
    color_max = 0
    for color in colors:
        if color_max < colors[color]:
            color_max =  colors[color]
    return color_max + 1