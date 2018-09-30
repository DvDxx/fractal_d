import networkx as nx
from fractal_model import fractal_model
from box_cover import GC, MEMB, cover_with_radius,renomolize_with_radius,renomolize_GC
from Network_efficiency import cal_E_glob
import pro_draw
import matplotlib.pyplot as plt
import multiprocessing
import read_write
import time

procees_num = 2


def model_test(g, n, m, e):
    G = fractal_model(g, n, m, e)
    print('Nodes:', nx.number_of_nodes(G))
    print('Edges:', nx.number_of_edges(G))
    at_least_box_number = nx.number_connected_components(G)
    N_times = 1000
    for i in range(N_times):
        X = []
        Y = []
        lb = 1
        X.append(lb)
        Y.append(G.number_of_nodes())
        while Y[-1] != at_least_box_number:
            lb += 1
            X.append(lb)
            Y.append(cover_with_radius(G, lb))
        print('%.1f%%' % (i * 100 / N_times))
        read_write.write_y('%d_%d_%d_%d' % (g, n, m, e), i, Y)
        # pro_draw.log_fit(X, Y,fn,show = 0)


def multi_model_test(lock, g, n, m, e, progress):
    G = fractal_model(g, n, m, e)
    print('Nodes:', nx.number_of_nodes(G))
    print('Edges:', nx.number_of_edges(G))
    at_least_box_number = nx.number_connected_components(G)
    return_dict = dict()
    N_times = int(1000 / procees_num)
    for i in range(N_times):
        X = []
        Y = []
        lb = 1
        X.append(lb)
        Y.append(G.number_of_nodes())
        while Y[-1] != at_least_box_number:
            lb += 1
            X.append(lb)
            Y.append(cover_with_radius(G, lb))
        return_dict[i] = Y
        lock.acquire()
        try:
            progress.value += 1 / procees_num
            print('%.3f%%' % (progress.value * 100 / N_times))
        finally:
            lock.release()
    return return_dict


def cal_model(g, n, m, e):
    mg = multiprocessing.Manager()
    progress = mg.Value('f', 0)
    time_start = time.time()
    lock = multiprocessing.Manager().Lock()
    pool = multiprocessing.Pool(processes=procees_num)
    result = dict()
    for i in range(procees_num):
        result[i] = pool.apply_async(multi_model_test, (lock, g, n, m, e, progress,))
        time.sleep(0.1)
    pool.close()
    pool.join()
    read_write.write_pro_y('%d_%d_%d_%.1f' % (g, n, m, e), result)
    print('spend time:', time.time() - time_start)

def dolphins_test():
    G = nx.read_gml('./data\\graph\\dolphins.gml')
    print('Nodes:', nx.number_of_nodes(G))
    print('Edges:', nx.number_of_edges(G))
    at_least_box_number = nx.number_connected_components(G)
    N_times = 1000
    store_dict = {}
    for i in range(N_times):
        X = []
        Y = []
        lb = 1
        X.append(lb)
        Y.append(G.number_of_nodes())
        while Y[-1] != at_least_box_number:
            lb += 1
            X.append(lb)
            Y.append(cover_with_radius(G, lb))
        print('%.1f%%' % (i * 100 / N_times))
        store_dict[i] = Y
    read_write.write_y('dolphins', store_dict)
        # pro_draw.log_fit(X, Y,fn,show = 0)

def renomal_eff():
    G = nx.Graph()
    node_index = 1
    for i in range(3):
        G.add_edge(0,node_index)
        node_index += 1
    nodes_degree = list(nx.degree(G))
    print(nx.global_efficiency(G))
    for degree in nodes_degree:
        for i in range(2*degree[1]):
            G.add_edge(degree[0], node_index)
            node_index += 1
    print(nx.global_efficiency(G))

if __name__ == '__main__':
    # cal_model(8, 3, 2, 0.3)
    # model_test(8, 3, 2, 0)
    Y = []
    # G = nx.read_gml('./data\\graph\\dolphins.gml')
    G = fractal_model(4,6,3,0)
    for i in range(100):
        print(G.number_of_nodes())
        Y.append(cal_E_glob(G))
        G = renomolize_GC(G,3)
        #nx.draw(G)
        #plt.show()
        if (G.number_of_nodes() == 1):
            break
    # for i in range(1):
    #     G = fractal_model(4, 6, 3, 1)
    #     for i in range(100):
    #         print(G.number_of_nodes())
    #         if i < len(Y):
    #             Y[i] += cal_E_glob(G)
    #         if (G.number_of_nodes() == 1):
    #             break
    #         G = renomolize_GC(G,2)
    print(Y)
    pro_draw.draw_y(Y,log = 1)