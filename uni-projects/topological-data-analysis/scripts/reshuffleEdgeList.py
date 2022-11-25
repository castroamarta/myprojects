#!/usr/bin/env python
# encoding=utf8
import networkx as nx
import sys
import random

# Outputs reshuffled versions of edgeLists

def readEdgeList(path_in):
    with open(path_in, "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [c.split() for c in content]
    [edgeList.append((int(edge[0]),int(edge[1]),float(edge[2]))) for edge in content]
    return edgeList

def weightReshuffle(edgeList):
    new_edgeList, weights = [], []
    for subl in edgeList:
        weights.append(subl[2])
    random.shuffle(weights)
    for i in range(len(edgeList)):
        new_edgeList.append([edgeList[i][0], edgeList[i][1], weights[i]])
    return new_edgeList

def doubleEdgeSwap(edgeList):
    new_edgeList = []
    weights = []
    G = nx.Graph()
    for edge in edgeList:
            u, v, weight = edge[0], edge[1], edge[2]
            weights.append(weight)
            G.add_edge(u,v)
    nx.double_edge_swap(G)
    edges =  list(G.edges())
    for i in range(len(edges)):
        new_edgeList.append([edges[i][0], edges[i][1],weights[i]])
    return new_edgeList

def outputReshuffled(edgeList, path_out):
    edgeList.sort(key = lambda x: (x[2],x[0],x[1]), reverse = True)
    sys.stdout = open(path_out, 'w')
    for edge in edgeList:
        u, v, w = edge[0], edge[1], edge[2]
        sys.stdout.write(str(u)),
        sys.stdout.write(" "),
        sys.stdout.write(str(v)),
        sys.stdout.write(" "),
        sys.stdout.write(str(w)),
        sys.stdout.write("\n")    

path_in = "/home/marta/WRCF/subject010/edgeLists/truncated_edgeList010.txt"
edgeList = []
edgeList = readEdgeList(path_in)
edgeList = weightReshuffle(edgeList) # null model 1
edgeList = doubleEdgeSwap(edgeList) # null model 2
path_out = "/home/marta/WRCF/subject010/edgeLists/edge_weight_reshuffle_eList010.txt"
outputReshuffled(edgeList, path_out)
