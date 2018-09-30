from math import cos,pi
from pro_draw import draw_xy

def Generate_WCF(gama, H, N):
    t = [i/(N-1) for i in range(N)]
    Kmax = 100
    series = []
    for i in t:
        Wt = [cos(2*pi*i*gama**(k))*(gama**((-1)*(k*H))) for k in range(1,Kmax)]
        series.append(sum(Wt))
    return  series

if __name__ == '__main__':
    series = Generate_WCF(5,0.3,1000)
    print(series)
    t = [i for i in range(1000)]
    draw_xy(t,series)