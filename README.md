# fractal dimension of complex networks

DvDxx
https://github.com/DvDxx/fractal_d

Some python programs for calculating fractal dimension of complex networks or graph structure. 

## Usage
# http://www-personal.umich.edu/~mejn/netdata/dolphins.zip
import networkx as nx
import GC from box_cover

G = nx.read_gml("./dophins.gml")
X, Y = GC(G)
