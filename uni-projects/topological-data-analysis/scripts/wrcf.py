#!/usr/bin/env python
# encoding=utf8
import networkx as nx
import sys
import random

# Outputs a .m file with the explicit definition of the simplices added at each step
# The output is written so that it can be used in javaplex

def readEdgeList():
    with open("edgeListText.txt", "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [c.split() for c in content]
    [edgeList.append((int(edge[0]),int(edge[1]),float(edge[2]))) for edge in content]
    return edgeList

def getBirthTimes():
    birthTimes = []
    previousBirth = 0
    for edge in edgeList:
        actualBirth = edge[2]
        if actualBirth != previousBirth:
            birthTimes.append(actualBirth)
            previousBirth = edge[2]
    return birthTimes

def findMaxCliques():
    cliques, aux =  [], list(nx.find_cliques(G_i)) # get all maximal cliques
    [cliques.append(clique) for clique in aux if len(clique) > 1]
    return cliques

def powerset(seq):
    if len(seq) <= 1:
        yield seq
        yield []
    else:
        for item in powerset(seq[1:]):
            yield [seq[0]]+item
            yield item

def getPowerset(seq):
    n = []
    s = [x for x in powerset(seq) if len(x) != len(seq) and len(x) != 0 and len(x) != 1]
    for i in s:
        i.sort(reverse = True)
        n.append(i)
    return n

def printClique(clique):
    sys.stdout.write("stream.addElement(["),
    for v in clique:
        if v != clique[-1]:
            sys.stdout.write(str(v)+','),
        else:
           sys.stdout.write(str(v)),
    sys.stdout.write("],"+str(step)+");\n")

edgeList = []
edgeList = readEdgeList()
n_nodes = 116
birthTimes = getBirthTimes()
maximum_filtration_value = 1297
edgeList.sort(key = lambda x: (x[2],x[0],x[1]), reverse = True)
G_i = nx.Graph()
[G_i.add_node(i) for i in range(n_nodes)]
nodes = list(G_i.nodes())

path = '/home/marta/WRCF/out.m'
sys.stdout = open(path, 'w')
sys.stdout.write("diary output.txt\n")
sys.stdout.write("diary on\n")
sys.stdout.write("import edu.stanford.math.plex4.*;\n")
sys.stdout.write("stream = api.Plex4.createExplicitSimplexStream();\n")
step = 0
for node in nodes:
    sys.stdout.write("stream.addVertex("+str(node)+","+str(step)+");\n")
step = 1
added_cliques = []
for time in birthTimes:
    if step < maximum_filtration_value:
        for edge in edgeList:
            weight = edge[2]
            if weight == time:
                u, v = edge[0], edge[1]
                e = [u,v]
                e.sort(reverse = True)
                added_cliques.append(e)
                printClique(e)
                G_i.add_edge(u,v)
                cliques = findMaxCliques()
                if len(cliques) > 0:
                    if len(added_cliques) == 0:
                        cliques[0].sort(reverse = True)
                        added_cliques.append(cliques[0])
                        printClique(cliques[0])
                    else:
                        for clique in cliques:
                            clique.sort(reverse = True)
                            if clique not in added_cliques:
                                added_cliques.append(clique)
                                printClique(clique)
                                s = getPowerset(clique) # add missing faces
                                for elem in s:
                                    if elem not in added_cliques:
                                        added_cliques.append(elem)
                                        printClique(elem)
        step = step + 1

sys.stdout.write("stream.finalizeStream();\n")
sys.stdout.write("persistence = api.Plex4.getModularSimplicialAlgorithm(3, 2);\n")
sys.stdout.write("intervals = persistence.computeAnnotatedIntervals(stream)\n")
sys.stdout.write("options.filename = \'Barcode\';\n")
sys.stdout.write("options.file_format = \'png\';\n")
sys.stdout.write("options.max_filtration_value = "+str(step)+";\n")
sys.stdout.write("plot_barcodes(intervals, options);\n")
sys.stdout.write("diary off\n")
