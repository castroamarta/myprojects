#!/usr/bin/env python
# encoding=utf8
import networkx as nx
import sys
import random

# Outputs truncated edgeList based on the edge added in the last filtration step

def readEdgeList(path_in):
    with open(path_in, "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [c.split() for c in content]
    [edgeList.append((int(edge[0]),int(edge[1]),float(edge[2]))) for edge in content]
    return edgeList

def truncateEdgeList(edgeList, path_out):
    edgeList = []
    edgeList = readEdgeList()
    edgeList.sort(key = lambda x: (x[2],x[0],x[1]), reverse = True)
    c = 0
    last_edge = [102,72] # add it manually, depends on the network
    count = 0
    for edge in edgeList:
        u, v = int(edge[0]), int(edge[1])
        if u == int(last_edge[0]) and v == int(last_edge[1]) or v == int(last_edge[0]) and u == int(last_edge[1]):
            c = count
        else:
            count = count + 1
    sys.stdout = open(path_out, 'w')
    for i in range(len(edgeList)):
        edge = edgeList[i]
        if i < c:
            u, v, w = edge[0], edge[1], edge[2]
            sys.stdout.write(str(u)),
            sys.stdout.write(" "),
            sys.stdout.write(str(v)),
            sys.stdout.write(" "),
            sys.stdout.write(str(w)),
            sys.stdout.write("\n")

path_in = "/home/marta/WRCF/subject010/edgeLists/edgeList010.txt"
e = readEdgeList(path_in)
path_out = "/home/marta/WRCF/subject010/edgeLists/truncated_edgeList010.txt"
truncateEdgeList(e,path_out)
