import networkx as nx
from itertools import combinations
from fbm import FBM
import pro_draw

def VG(series):
    g = nx.Graph()
    # convert list of magnitudes into list of tuples that hold the index
    t_series = []
    n = 0
    for magnitude in series:
        t_series.append((n, magnitude))
        n += 1

    # contiguous time points always have visibility
    for n in range(0, len(t_series) - 1):
        (ta, ya) = t_series[n]
        (tb, yb) = t_series[n + 1]
        g.add_node(ta, mag=ya)
        g.add_node(tb, mag=yb)
        g.add_edge(ta, tb)
    ss = combinations(t_series, 2)
    for a, b in ss:
        # two points, maybe connect
        (ta, ya) = a
        (tb, yb) = b
        connect = True
        # let's see all other points in the series
        for tc, yc in t_series:
            # other points, not a or b
            if tc <= ta:
                continue
            if tc >=tb:
                break
                # does c obstruct?
            if yc > yb + (ya - yb) * ((tb - tc) / (tb - ta)):
                connect = False
                break
        if connect:
            g.add_edge(ta, tb)
    return g

def HVG(series):
    '''
    function HVG(series) convert time series to horizon visibility graph
    :return:networkx graph from time series
    '''
    N = len(series)
    G = nx.Graph()
    for ta in range(N):
        ya = series[ta]
        criterion = 0
        for tb in range(ta + 1, N):
            yb = series[tb]
            if yb >= criterion:
                if ya >= criterion:
                    criterion = yb
                    G.add_edge(ta,tb)
                else:
                    break
                    #edge_list.append([ta, tb])
    return G

if __name__ == '__main__':
    f = FBM(n=1000, hurst=0.5, length=1, method='daviesharte')
    #series = [x for x in range(50)]
    series = f.fbm()
    #series = [2,4,1,5,6,3,6]
    G = HVG(series)
    pro_draw.draw_graph(G)
    #print(G.number_of_edges())

