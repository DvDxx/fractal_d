# fractal dimension of complex networks

DvDxx
https://github.com/DvDxx/fractal_d

Some python programs for calculating fractal dimension of complex networks or graph structure. 

## Usage
Test code example
```
# http://www-personal.umich.edu/~mejn/netdata/dolphins.zip
import networkx as nx
import GC from box_cover
import matplotlib.pyplot as plt
\# test code
G = nx.read_gml("./dophins.gml")
X, Y = GC(G)
LogXI = [np.log10(x) for x in X]
LogYI = [np.log10(y) for y in Y]
z1 = np.polyfit(LogXI, LogYI, 1)
fractal_dimension = z1[0] # The fractal dimension is the slope of the fitting line z1
print("fractal dimension = ",fractal_dimension)
yvals = p1(LogXI)
plt.plot(LogXI , LogYI ,'o', markersize=15)
plt.plot(LogXI , yvals,'-', markersize=15, linewidth=3)
plt.show()
```
