from __future__ import print_function
from igraph import *
import igraph
import sys
import random
import time

# Implementation of Kruskal algorithm for complexity analysis

class Node:
    def __init__ (self, label):
        self.label = label
    def __int__(self):
        return self.label

def initialDisjointSets(node):
     node.parent = node
     node.rank   = 0

def findParent(node):
	if node.parent == node:
		return node
	else:
		return findParent(node.parent)

def unionByRank(node1,node2):
	root1 = findParent(node1)
	root2 = findParent(node2)
	if root1 == root2:
		return -1
	elif root1.rank <= root2.rank:
		root1.parent = root2
		root2.rank += 1
	elif root1.rank > root2.rank:
		root2.parent = root1
		root1.rank += 1

def randomGraphGenerator(numberNodes, probability):

	g = Graph().Erdos_Renyi(numberNodes, probability, directed = False, loops = False)
	nlist = []
	for e in g.es:
		nlist.append([e.tuple[0],e.tuple[1],random.randint(0,10)])

	return nlist

##### random graph for complexity analysis, choose number of nodes and probability
nNodes = 700
probability = 0.3
nlist = randomGraphGenerator(nNodes, probability)

start_time = time.time()

nlist.sort(key = lambda x: (x[2],x[0],x[1])) # defines total order in the list

lNodes = [Node(num) for num in range(1,nNodes + 1)]

for node in lNodes:
	initialDisjointSets(node)

sets =  [int(findParent(i)) for i in lNodes]

nodes = []
for i in nlist:
	for j in lNodes:
		if int(j) == i[0]:
			for k in lNodes:
				if int(k) == i[1]:
					if unionByRank(k,j) != -1:
						nodes.append([int(k),int(j)])

for i in nodes:
	if i[0] > i[1]:
		i[0], i[1] = i[1], i[0]

nodes = sorted(nodes, key = lambda x: (x[0],x[1]))
for i in nodes:
	print(i[0]," ",i[1])

print("--- %s seconds ---" % (time.time() - start_time))
