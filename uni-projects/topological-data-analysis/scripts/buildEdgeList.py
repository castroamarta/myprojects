import csv
import numpy as np
import networkx as nx

# Outputs edgeList based on the positive entries of the association matrix

def readFile(path):
    with open(path,'r') as file:
        content = csv.reader(file)
        l = []
        for row in content:
            l.append(row)
    file.close()
    return l

# consideres only positive coeficients
def buildEdgeList(l,threshold):
    dim = len(l[0])
    adj = np.zeros((dim,dim))
    for r in range(dim):
        for c in range(dim):
            curr = float(l[r][c])
            val = curr
            if val > threshold:
                adj[r][c] = val
            else:
                adj[r][c] = 0
    edgeList = []
    for r in range(dim):
        for c in range(r+1,dim):
            val = adj[r][c]
            if val != 0:
                edgeList.append([r,c,val])
    return edgeList

def writeEdgeList(edgeList,n_nodes,path_out):
    file = open(path_out,"w")
    edgeList.sort(key = lambda x: (x[2],x[0],x[1]), reverse = True)
    for edge in edgeList:
        print >> file, str(edge[0])+' '+str(edge[1])+' '+str(edge[2])
    file.close()


path_in = '/home/marta/WRCF/subject010/roi_corr/sub-010_r_matrix.csv'
a = readFile(path_in)
threshold = 0
edgeList = buildEdgeList(a,threshold)
n_nodes = 116
path_out = '/home/marta/WRCF/subject010/edgeLists/edgeList010.txt'
writeEdgeList(edgeList,n_nodes,path_out)
