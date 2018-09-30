import networkx as nx
from fractal_model import fractal_model
import time

def cal_E_glob(G,subgraph = None):
    E_glob = 0
    N = len(G)
    node_list = list(G.nodes())
    if subgraph:
        node_list = subgraph
        N = len(subgraph)
        node_index = 0
        for source in node_list:
            node_index += 1
            for target in node_list[node_index:]:
                dij = nx.shortest_path_length(G, source=source, target=target)
                E_glob += 1 / dij
    else:
        shotest_path = dict(nx.shortest_path_length(G))
        node_index = 0
        for source in node_list:
            node_index += 1
            for target in node_list[node_index:]:
                dij = shotest_path[source][target]
                E_glob += 1 / dij
    return E_glob*2/(N*(N-1))

def cal_E_local(G):
    N = G.number_of_nodes()
    E_local = 0
    node_list = list(G.nodes())
    for node in node_list:
        sub_node = list(G[node])
        sub_node.append(node)
        E_local += cal_E_glob(G,sub_node)
    return E_local/N


if __name__ =='__main__':

    # G = nx.to_undirected(nx.read_weighted_edgelist('./data\\graph\\out.moreno_mac_mac'))
    # G = nx.read_adjlist('./data\\graph\\NDwww.net')
    # G = nx.read_gml('./data\\graph\\celegansneural.gml')
    G = nx.read_gml('./data\\graph\\dolphins.gml')
    print(cal_E_glob(G))
    print(cal_E_local(G))