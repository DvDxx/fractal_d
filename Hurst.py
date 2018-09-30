import numpy as np
import math
import pandas as pd
from fbm import FBM
import hurst
from numpy import std, subtract, polyfit, sqrt, log
from pro_draw import draw_y,draw_xy,log_draw_xy
import matplotlib.pyplot as plt

from visibility_graph import VG,HVG
from box_cover import GC
import networkx as nx
from WCF import Generate_WCF
import time




def hurst1(ts):
    ts = list(ts)
    N = len(ts)
    if N < 20:
        raise ValueError("Time series is too short! input series ought to have at least 20 samples!")

    max_k = int(np.floor(N / 2))
    R_S_dict = []
    for k in range(10, max_k+1):
        R, S = 0, 0
        # split ts into subsets
        subset_list = [ts[i:i + k] for i in range(0, N, k)]
        if np.mod(N, k) > 0:
            subset_list.pop()
            # tail = subset_list.pop()
            # subset_list[-1].extend(tail)
        # calc mean of every subset
        mean_list = [np.mean(x) for x in subset_list]
        for i in range(len(subset_list)):
            cumsum_list = pd.Series(subset_list[i] - mean_list[i]).cumsum()
            R += max(cumsum_list) - min(cumsum_list)
            S += np.std(subset_list[i])
        R_S_dict.append({"R": R / len(subset_list), "S": S / len(subset_list), "n": k})

    log_R_S = []
    log_n = []
    print(R_S_dict)
    for i in range(len(R_S_dict)):
        R_S = (R_S_dict[i]["R"] + np.spacing(1)) / (R_S_dict[i]["S"] + np.spacing(1))
        log_R_S.append(np.log(R_S))
        log_n.append(np.log(R_S_dict[i]["n"]))
    draw_xy(log_n,log_R_S)
    Hurst_exponent = np.polyfit(log_n, log_R_S, 1)[0]
    return Hurst_exponent

def hurst2(ts):
    """Returns the Hurst Exponent of the time series vector ts"""

    # create the range of lag values
    i = len(ts) // 2
    lags = range(2, i)
    # Calculate the array of the variances of the lagged differences
    tau = [sqrt(std(subtract(ts[lag:], ts[:-lag]))) for lag in lags]

    # use a linear fit to estimate the Hurst Exponent
    poly = polyfit(log(lags), log(tau), 1)

    # Return the Hurst Exponent from the polyfit output
    return poly[0]*2

def repeat_task(series,N):
    f = FBM(n=10000, hurst=0.75, length=1, method='daviesharte')
    for i in range(N):
        H, c, data  = hurst.compute_Hc(f.fbm() + 10., kind='price', simplified=True)
        yield H

def repeat_by(func,N):
    all_times = func()
    for _ in range(N-1):
        count = 0
        for each in func():
            all_times[count] += each
            count += 1
        print(_)
    return [x/N for x in all_times]

def d_h_test(H=None,f=None):
    if not H:
        H = [x / 100 for x in range(1, 100)]
    fractal_d = []
    for h in H:
        if not f:
            f = FBM(n=2000, hurst=h, length=1, method='daviesharte')
        series = f.fbm()
        G = VG(series)
        #Y = nx.degree_histogram(G)
        #print(Y)
        X, Y = GC(G)
        LogXI, LogYI = [], []
        for x in X:
            LogXI.append(math.log(x))
        for y in Y:
            LogYI.append(math.log(y))
        fractal_d.append(-1 * np.polyfit(LogXI, LogYI, 1)[0])
        #print(Y)
    return fractal_d

if __name__ == '__main__':
    # random_changes = 1. + np.random.randn(500) / 1000.
    # f = FBM(n=5000, hurst=0.5, length=1, method='daviesharte')
    #series = hurst.random_walk(10000,proba=0.3)
    #H = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    H = [0.05*i for i in range(1,19)]
    core_n = []
    for h in H:
        f = FBM(n=1000, hurst=h, length=1, method='daviesharte')
        # series = Generate_WCF(5,h,2000)
        series = f.fbm()
        G = HVG(series)
        X,Y = GC(G)
        log_draw_xy(X,Y)
        #core_n.append(nx.k_core(G).number_of_nodes())
    #print(core_n)

    #     X,Y = GC(G)
    #     LogXI, LogYI = [], []
    #     for x in X:
    #         LogXI.append(math.log(x))
    #     for y in Y:
    #         LogYI.append(math.log(y))
    #     fractal_d.append(-1 * np.polyfit(LogXI, LogYI, 1)[0])
    # X =[]
    # for i in range(1,len(H)+1):
    #     X.append(i)
    # log_draw_xy(X,fractal_d)
    # fd = []
    # for h in H:
    #     fd.append(2-h)
    # log_draw_xy(fd,fractal_d)
    #print(hurst1(series))
    #hurst1(list(range(1,50)))
    # print(hurst2(series))
    # H, c, data = hurst.compute_Hc(series, kind='random_walk', simplified=True)
    # print(H)
    # print(d_h_test(f=f))
    # series = np.cumprod(random_changes)
    # H = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    #Y = repeat_by(d_h_test,100)
    #H = [x / 100 for x in range(1, 100)]
    #draw_xy(H,Y)
