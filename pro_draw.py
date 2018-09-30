import math
import matplotlib.pyplot as plt
import numpy as np
import os
import networkx as nx
import read_write
import pickle

def log_fit(X, Y, fn=None, show = 1):
    LogXI = []
    LogYI = []
    for i in range(0, len(X)):
        LogXI.append(math.log(X[i]))
    for i in range(0, len(Y)):
        LogYI.append(math.log(Y[i]))
    z1 = np.polyfit(LogXI, LogYI, 1)  # 一次多项式拟合，相当于线性拟合
    p1 = np.poly1d(z1)
    yvals = p1(LogXI)
    print(p1)
    plot1 = plt.plot(LogXI, LogYI, 'ro', label='original values', markersize=6, linewidth=2)
    plot2 = plt.plot(LogXI, yvals, 'b', label='polyfit values', markersize=10, linewidth=6)
    plt.xlabel(r'$\mathrm{ln(l_B)}$', fontsize=15)
    plt.ylabel(r'$\mathrm{ln(N_B)}$', fontsize=15)
    for label in plt.gca().xaxis.get_ticklabels():
        label.set_fontsize(10)
    for label in plt.gca().yaxis.get_ticklabels():
        label.set_fontsize(10)
    plt.legend()  # 指定legend的位置,可以参考help的用法
    if fn:
        if not os.path.exists('./data\\' + fn):
            os.makedirs('./data\\' + fn)
        path_dir = './data\\' + fn + '\\'
        plt.savefig(path_dir + fn+'.png')
    if show:
        plt.show()

def log_draw_xy(X,Y):
    LogXI = []
    LogYI = []
    for x in X:
        LogXI.append(math.log(x))
    for y in Y:
        LogYI.append(math.log(y))
    draw_xy(LogXI,LogYI)

def draw_xy(X,Y):
    z1 = np.polyfit(X, Y, 1)  # 一次多项式拟合，相当于线性拟合
    p1 = np.poly1d(z1)
    yvals = p1(X)
    print(p1)
    #plot1 = plt.plot(X, Y, 'ro', label='original values', markersize=8, linewidth=15)
    plot1 = plt.plot(X, Y, linewidth=3)
    #plot2 = plt.plot(X, yvals, 'b', label='polyfit values', markersize=10, linewidth=6)
    #plt.xlabel(r'$\mathrm{ln(l_B)}$', fontsize=15)
    #plt.ylabel(r'$\mathrm{ln(N_B)}$', fontsize=15)
    for label in plt.gca().xaxis.get_ticklabels():
        label.set_fontsize(10)
    for label in plt.gca().yaxis.get_ticklabels():
        label.set_fontsize(10)
    plt.legend()  # 指定legend的位置,可以参考help的用法
    #plt.title('England')
    plt.show()

def draw_y(Y,log = 1):
    count = 1
    X = []
    for i in Y:
        X.append(count+1)
        count += 1
    if log:
        new_X = []
        new_Y = []
        for i in range(len(Y)):
            if Y[i] != 0:
                new_X.append(X[i])
                new_Y.append(Y[i])
        log_draw_xy(new_X, new_Y)
    else:
        draw_xy(X, Y)

def draw_graph(G):
    nx.draw(G)
    plt.show()

if __name__ == '__main__':
    #Y = read_write.read_avg_y('7_4_2_0','A521:CY521')
    Y = [35, 10, 33, 24, 25, 58, 20, 12, 27, 41, 65, 46, 40, 40, 67, 76, 148, 72]
    count = 1
    X = []
    for i in Y:
        X.append(count+1)
        count += 1
    draw_xy(X,Y)