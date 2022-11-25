#!/usr/bin/env python
# coding=utf-8
import sys
import re
import itertools
from sys import stdout
from subprocess import call

# Implementation of the border gateway protocol
# Input: number of nodes, maximum cost and contracts
# Output: .pml file that serves as input to Spin
# Run using: ./BGP.py < input.txt

def readInputFile():

	textline = [line.strip() for line in sys.stdin]

	n_nodes = int(textline[0])
	maxCost = int(textline[1])

	lines = []

	[lines.append(j) for j in [i.split('\t') for i in textline[2:]]]

	edgeList = []

	[edgeList.append(map(int,lines[i][0].split(" "))) for i in range(len(lines))]

	contractList = []

	[contractList.append([map(int,lines[i][0].split(" ")),map(int,lines[i][1].split(" "))]) for i in range(len(lines))]

	return n_nodes, maxCost, edgeList, contractList

def buildNodeList(n_nodes):

	nodeList = []
	for node in range(n_nodes):
		nodeList.append(node)

	return nodeList

# to return all paths that have no cycles in them
def allPaths(n_nodes, nodeList):

	allSubSets = []
	for i in range(1, len(nodeList) + 1):
	    for subset in itertools.combinations(nodeList, i):
	    	if len(subset) >= 2:
	        	allSubSets.append(list(list(subset)))

	paths = []
	for subset in allSubSets:
		aux1 = list(itertools.permutations(subset))
		aux2 = [list(elems) for elems in aux1]
		paths.append(aux2)

	allPaths = []
	for path in paths:
		for r in path:
			allPaths.append(r)

	return [[0]] + allPaths

def getUnreachablePath(idx):

	unreachable = 0
	for pathIdx in range(len(idx)):

		unreachable = pathIdx + 1

	return unreachable

def possiblePaths(n_nodes, edgeList, allPaths, target):

	possiblePaths = []
	for path in allPaths: # remove the target initial path
		for edge in edgeList:

			if len(path) == 2:
				# chose paths that lead to target
				if path[0] == edge[0] and path[1] == edge[1] and path[-1] == target:
					possiblePaths.append(path)
			else:
				for i in range(len(path)-1):
					for j in range(i+1, len(path)):
						if j == i + 1:
							# chose paths that lead to target
							if i == edge[0] and j == edge[1] and path[-1] == target:
								possiblePaths.append(path)

	return [[0]] + possiblePaths

def pathAsInt(possiblePaths):

	idx = []
	i = 0
	for path in possiblePaths:
		idx.append([path,i])
		i = i + 1
	return idx

def addNodeToPath(idx, path, node):

	for i in idx:
		if i[1] == path:
			return [node] + i[0]

def newPathToReturn(idx, path):

	for k in idx:
		if path == k[0]:
			return k[1]

def outDegree(node, edgeList):

	count = 0
	for edge in edgeList:
		if edge[0] == node:
			count = count + 1
	return count

def outNodes(node, edgeList):

	outNodes = []
	for edge in edgeList:
		if edge[0] == node:
			outNodes.append(edge[1])

	return outNodes

def inNodes(node, edgeList):

	inNodes = []
	for edge in edgeList:
		if node == edge[1]:
			inNodes.append(edge[0])
	return inNodes

def contract(node1, node2, cost, lcontracts):

	for l in lcontracts:
		if l[0][0] == node1 and l[0][1] == node2:
			for c in range(len(l[1])):
				if c == cost:
					return l[1][c]

def printChannels(edgeList, target, file):

	for node in nodeList:
		lin = inNodes(node,edgeList)
		if node == target:
			for inNode in lin:
				print >> file, "chan t"+str(node)+str(inNode)+" = [2] of {byte,byte}"
		else:
			for inNode in lin:
				print >> file, "chan c"+str(node)+str(inNode)+" = [2] of {byte,byte}"

	print >> file, "\n"

def printVerificationCondition(edgeList, nodeList, target, file):

	print >> file, "ltl p1{ <>[](",
	for node in nodeList:
		lin = inNodes(node,edgeList)
		if node == target:
			for inNode in lin:
				print >> file, "len(t"+str(node)+str(inNode)+")=="+str(0)+" &&",

		else:
			for inNode in lin:
				if inNode == lin[-1] and node == nodeList[-1]:
					print >> file, "len(c"+str(node)+str(inNode)+")=="+str(0)+" ) }"
				else:
					print >> file, "len(c"+str(node)+str(inNode)+")=="+str(0)+" &&",

def printTargetProcess(edgeList,x,y,file):

	print >> file, "\nactive proctype t(){\n"
	for edge in edgeList:
		if edge[1] == target:
			print >> file, "t"+str(target)+str(edge[0])+"!"+str(x)+","+str(y)+";\n"

	print >> file, "}\n"

def printSendMessage(node, edgeList, file):

	lin = inNodes(node, edgeList)
	for inNode in lin:
		if inNode == lin[-1]:
			print >> file, "c"+str(node)+str(inNode)+" ! cost,path\n"
		else:
			print >> file, "c"+str(node)+str(inNode)+" ! cost,path;",


def printNodesProcesses(edgeList,nodeList,maxCost, unreachable,target, lcontracts,idx, file):

	for node in nodeList:

		count = 1

		if node != target:

			print >> file, "\nactive proctype n"+str(node)+"(){\n"

			print >> file, "byte x = 0;"
			print >> file, "byte y = 0;\n"
			print >> file, "byte path;\n"
			print >> file, "byte cost;\n"

			aux = outDegree(node,edgeList)
			print >> file, "byte v"+str(node)+"["+str(aux)+"];"
			print >> file, "byte p"+str(node)+"["+str(aux)+"];"

			# initialize history array with max cost and unreachable path
			for outEdge in range(aux):
				print >> file, "v"+str(node)+"["+str(outEdge)+"] = "+str(maxCost)+";"
				print >> file, "p"+str(node)+"["+str(outEdge)+"] = "+str(unreachable)+";"

			print >> file, "\n"
			print >> file, "do\n"

			lout = outNodes(node, edgeList)
			for outNode in lout:
				if outNode == target:

					###### read from target ######

					print >> file, "\n:: t"+str(target)+str(node)+" ? "+"x,y;\n"

					# the only path the target can send is the path containing it self: 0

					path  = 0
					aux1 = addNodeToPath(idx, path, node)
					newPath = newPathToReturn(idx, aux1)

					print >> file, "\tif\n"
					print >> file, "\t:: (y == "+str(path)+") -> y = "+str(newPath)+";\n"

					###### costs ######

					print >> file, "\t\tif\n"
					for cost in range(maxCost + 1):

						print >> file, "\t\t::(x == "+str(cost)+") -> "+"cost = "+str(contract(node, target, cost, lcontracts))+";\n"

						## update ##

						print >> file, "\t\t\tif\n"


						print >> file, "\t\t\t\t::(cost < v"+str(node)+"["+str(target)+"]) -> v"+str(node)+"["+str(target)+"] = cost; p"+str(node)+"["+str(target)+"] = path;",

						# send to all others

						printSendMessage(node, edgeList, file)

						print >> file, "\t\t\tfi\n"

					print >> file, "\t\tfi\n"

					###### invalid path not unreachable -> reset ######

					print >> file, "\t:: (y != 0 && y != "+str(unreachable)+")\n"

					print >> file, "\t\tif\n"
					print >> file, "\t\t\t:: (p"+str(node)+"["+str(target)+"] != "+str(unreachable)+") -> cost = v"+str(node)+"["+str(target)+"]; path = p"+str(node)+"["+str(target)+"];",

					# send to all others

					printSendMessage(node, edgeList, file)

					print >> file, "\t\t\t:: else -> cost ="+str(maxCost)+"; path = "+str(unreachable)+";",

					# send to all others

					printSendMessage(node, edgeList, file)

					print >> file, "\t\tfi\n"


					#### case in which the path is unreachaable ####

					print >> file, "\t:: (y == "+str(unreachable)+")\n"
					print >> file, "\t\tif\n"

					print >> file, "\t\t\t:: (p"+str(node)+"["+str(target)+"] != "+str(unreachable)+") -> cost = v"+str(node)+"["+str(target)+"]; path = p"+str(node)+"["+str(target)+"];",

					# send to all others

					printSendMessage(node, edgeList, file)

					print >> file, "\t\tfi\n"


					print >> file, "\t:: else -> skip;\n"

					print >> file, "\tfi\n"

				else:

					###### read from outNodes ######

					print >> file, "\n:: c"+str(outNode)+str(node)+" ? "+"x,y;\n"

					# which are the paths that are valid and that I can read from this channel?
					# Here I can only read valid the paths that have the node of the channel that I am reading from and that end in the target

					print >> file,"\tif\n"
					for l in idx:
						if outNode in l[0] and node not in l[0]:

							path = l[1]
							aux1 = addNodeToPath(idx, path, node)
							newPath = newPathToReturn(idx, aux1)


							print >> file, "\t:: (y == "+str(path)+") -> y = "+str(newPath)+";\n"

							###### costs ######

							print >> file, "\t\tif\n"

							for cost in range(maxCost + 1):

								print >> file, "\t\t::(x == "+str(cost)+") -> "+"cost = "+str(contract(node, outNode, cost, lcontracts))+";\n"

								## update ##

								print >> file, "\t\t\tif\n"


								print >> file, "\t\t\t\t::(cost < v"+str(node)+"["+str(count)+"]) -> v"+str(node)+"["+str(count)+"] = cost; p"+str(node)+"["+str(count)+"] = path;",

								# send to all others

								printSendMessage(node, edgeList, file)

								print >> file, "\t\t\tfi\n"

							print >> file, "\t\tfi\n"

					###### invalid path not unreachable -> reset ######

					print >> file, "\t:: (y != 0 && y != "+str(unreachable)+")\n"

					print >> file, "\t\tif\n"
					print >> file, "\t\t\t:: (p"+str(node)+"["+str(count)+"] != "+str(unreachable)+") -> cost = v"+str(node)+"["+str(count)+"]; path = p"+str(node)+"["+str(count)+"];",

					# send to all others

					printSendMessage(node, edgeList, file)

					print >> file, "\t\t\t:: else -> cost ="+str(maxCost)+"; path = "+str(unreachable)+";",

					# send to all others

					printSendMessage(node, edgeList, file)

					print >> file, "\t\tfi\n"

					#### case in which the path is unreachaable ####

					print >> file, "\t:: (y == "+str(unreachable)+")\n"
					print >> file, "\t\tif\n"

					print >> file, "\t\t\t:: (p"+str(node)+"["+str(count)+"] != "+str(unreachable)+") -> cost = v"+str(node)+"["+str(count)+"]; path = p"+str(node)+"["+str(count)+"];",

					# send to all others

					printSendMessage(node, edgeList, file)

					print >> file, "\t\tfi\n"

					print >> file, "\t:: else -> skip;\n"

					print >> file, "\tfi\n"

					count = count + 1

			print >> file, "\nod\n"
			print >> file, "}"

# to get the output: cost x, path y and content from channels

def getOutput(nodeList, target, file):

	with open(file, 'r') as f:

   		lines = f.readlines()

	lx, ly = [], []
	target = 0
	for node in nodeList:
		if node != target:
			for line in lines:
				patternx = 'n'+str(node)+'\('+str(node)+'\):x'
				patterny = 'n'+str(node)+'\('+str(node)+'\):y'
				if re.search(patternx,line) != None:
					p = re.compile(r' \d+')
					aux2 = p.findall(line)
					lx.append([node,map(int,aux2)])
				if re.search(patterny,line) != None:
					p = re.compile(r' \d+')
					aux1 = p.findall(line)
					ly.append([node,map(int,aux1)])

	listx, listy = [], []

	[listx.append([x[0],x[1][0]]) for x in lx]
	[listy.append([y[0],y[1][0]]) for y in ly]


	l = []
	# get channel content from textfile
	for edge in edgeList:
		startNode, endNode = edge[0], edge[1]
		if endNode == target:
			patternt = '\('+'t'+str(endNode)+str(startNode)+'\)'+':'
			for line in lines:
				if re.search(patternt,line) != None:
					p = re.compile(r'\d+')
					l.append([endNode, startNode, p.findall(line)])
		else:
			patternc = '\('+'c'+str(endNode)+str(startNode)+'\)'+':'
			for line in lines:
				if re.search(patternc,line) != None:
					p = re.compile(r'\d+')
					l.append([endNode,startNode, p.findall(line)])


	# None if a channel is empty
	channels = []
	for i in l:
		for edge in edgeList:
			startNode, endNode = edge[0], edge[1]
			if i[0] == endNode and i[1] == startNode:
				if len(i[2]) == 2:
					channels.append([endNode, startNode, None])
				else:
					channels.append([endNode, startNode, map(int,i[2][-2:])])


	return listx, listy, channels

#**
# #contracts between node1 and node2 in the form: [[node1,node2],[0,2,...,maxCost], ...,[node2,node4],[0,...,maxCost]]
target = 0 # by definition target is always represented by 0
#**

# get Input from txt file

n_nodes, maxCost, edgeList, lcontracts = readInputFile()
nodeList = buildNodeList(n_nodes)
n_edges = len(edgeList)

# calls to process paths

allPaths = allPaths(n_nodes, nodeList)
possiblePaths = possiblePaths(n_nodes,edgeList,allPaths,target)
idx = pathAsInt(possiblePaths)
unreachable = getUnreachablePath(idx)


x = maxCost
y = unreachable

file = open("BGP.pml","w")

printChannels(edgeList, target, file)
printVerificationCondition(edgeList, nodeList, target, file)
printTargetProcess(edgeList,x,y,file)
printNodesProcesses(edgeList,nodeList,maxCost, unreachable,target, lcontracts,idx, file)

file.close()

# Call Spin and output channels:

# with open("result.txt", "w") as of:
# 	call(["/usr/local/bin/spin","-X","-l","-g","-o2","-n123","-u10000","BGP.pml"],stdout = of)

# listx, listy, channels = getOutput(nodeList, target, "result.txt")

# print channels
