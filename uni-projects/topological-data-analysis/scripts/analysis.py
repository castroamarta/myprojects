#!/usr/bin/env python
# encoding=utf8
from __future__ import division
import sys

# computes hollowness values and most persistent 1-cycles.
# Outputs files with births, persistences and lengths to compute distributions

def readJPoutput():
    path = "/home/marta/WRCF/subject006/javaplex_output/output006.txt"
    with open(path, "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [c.split() for c in content]
    return content

def computeLifetime(c):
    global cycle_life_time
    global birth
    for k in range(len(c)):
        if k == 0:
            birth = float(c[k].split('[')[1].split(',')[0])
        elif k == 1:
            u = c[k].split(')')[0]
            if u == 'infinity':
                cycle_life_time = maximum_filtration_value - birth
            else:
                cycle_life_time = float(u) - birth
    return birth, cycle_life_time

def findRepresentatives(aux,reps):
    a = aux.split(',')
    if len(a) == 2:
        u = int(a[0].split('[')[1])
        v = int(a[1].split(']')[0])
        if u not in reps:
            reps.append(u)
        if v not in reps:
            reps.append(v)
    elif len(a) == 3:
        u = int(a[0].split('[')[1])
        v = int(a[1])
        w = int(a[2].split(']')[0])
        if u not in reps:
            reps.append(u)
        if v not in reps:
            reps.append(v)
        if w not in reps:
            reps.append(w)

def computeCycleLength(c):
    count = 0
    reps = []
    for j in range(len(c)):
        if j > 1:
            aux = c[j]
            if aux[0] == "[":
                count = count + 1
                findRepresentatives(aux,reps)
            elif aux[0] == "-" and len(aux) > 1:
                if aux[1] == "[":
                    count = count + 1
                    findRepresentatives(aux,reps)
    reps.sort(reverse = True)
    return reps, count

def writeOutput():
    path = '/home/marta/WRCF/subject006/analysis/subject_6_'+str(network)+'_info.txt'
    sys.stdout = open(path, 'w')
    sys.stdout.write('Maximum Filtration Value: '+str(maximum_filtration_value)+"\n")
    sys.stdout.write('Cycles with persistence larger than '+str(thresh)+":\n")
    sys.stdout.write('(Persistence Birth Length Representatives)\n')
    if len(cycle_1_info) > 0:
        sys.stdout.write('\nDimension '+str(1)+':\n')
        cycle_1_info.sort(key = lambda x: (x[0],x[1],x[2],x[3]), reverse = True)
        for cycle in cycle_1_info:
            sys.stdout.write(str(cycle[0])+' '+str(cycle[1])+' '+str(cycle[2])+' '+str(cycle[3])+'\n')
    if len(cycle_2_info) > 0:
        sys.stdout.write('\nDimension '+str(2)+':\n')
        cycle_2_info.sort(key = lambda x: (x[0],x[1],x[2],x[3]), reverse = True)
        for cycle in cycle_2_info:
            sys.stdout.write(str(cycle[0])+' '+str(cycle[1])+' '+str(cycle[2])+' '+str(cycle[3])+'\n')
    sys.stdout.write('\nHollowness:\n')
    sys.stdout.write('\nDimension '+str(1)+':\n')
    sys.stdout.write(str(h_1))
    sys.stdout.write('\nNormalized hollowness:\n')
    sys.stdout.write(str(h_1_normalized)+'\n')
    sys.stdout.write('\nDimension '+str(2)+':\n')
    sys.stdout.write(str(h_2))
    sys.stdout.write('\nNormalized hollowness:\n')
    sys.stdout.write(str(h_2_normalized)+'\n')

def outputLists(l1,l2,l3,h_group,network):
    path = '/home/marta/WRCF/subject006/analysis/subject_6_distributions_'+str(h_group)+'_'+str(network)+'.txt'
    sys.stdout = open(path, 'w')
    sys.stdout.write('Briths:\n')
    for elem in l1:
        sys.stdout.write(str(elem/maximum_filtration_value)+' ') # normalize my the maximum filtration value
    sys.stdout.write('\n')
    sys.stdout.write('\nPersistences:\n')
    for elem in l2:
        sys.stdout.write(str(elem/maximum_filtration_value)+' ') 
    sys.stdout.write('\n')
    sys.stdout.write('\nLengths:\n')
    for elem in l3:
        sys.stdout.write(str(elem)+' ')
    sys.stdout.close()

# original, w_r or e_w_r
network = 'original'
content = readJPoutput()
n_of_homology_groups = 2
maximum_filtration_value = 1296 # change manually
thresh = maximum_filtration_value/2
N = 116 # number of nodes
representatives = []
cycle_1_info, cycle_1_births, cycle_1_persistences, cycle_1_lengths = [], [], [], []
cycle_2_info, cycle_2_births, cycle_2_persistences, cycle_2_lengths = [], [], [], []
for i in range(len(content)):
    k = 0
    if len(content[i]) > 1:
        if content[i][0] == 'Dimension:':
            cycle_count = 0
            if content[i][1] == str(1):
                k = i + 1
                sum_cycles = 0
                sum_lengths = 0
                while content[k][0] != 'Dimension:':
                    c = content[k]
                    cycle_count = cycle_count + 1
                    brith, cycle_life_time = computeLifetime(c)
                    rep, cycle_length = computeCycleLength(c)
                    cycle_1_births.append(birth)
                    cycle_1_lengths.append(cycle_length)
                    cycle_1_persistences.append(cycle_life_time)
                    if cycle_life_time > thresh:
                        if rep not in representatives:
                            representatives.append(rep)
                            cycle_1_info.append([cycle_life_time,birth,cycle_length,rep])
                        sum_lengths = sum_lengths + cycle_length
                        sum_cycles = sum_cycles + cycle_life_time
                    else:
                        sum_lengths = sum_lengths + cycle_length
                        sum_cycles = sum_cycles + cycle_life_time
                    k = k + 1
                h_1 = (1/cycle_count)*(sum_cycles/maximum_filtration_value)
                h_1_normalized = (1/cycle_count)*(sum_lengths/N)*(sum_cycles/maximum_filtration_value)
            elif content[i][1] == str(n_of_homology_groups):
                k = i + 1
                sum_cycles = 0
                sum_lengths = 0
                while k < len(content):
                    cycle_count = cycle_count + 1
                    c = content[k]
                    if len(c) > 2:
                        brith, cycle_life_time = computeLifetime(c)
                        rep, cycle_length = computeCycleLength(c)
                        cycle_2_births.append(birth)
                        cycle_2_lengths.append(cycle_length)
                        cycle_2_persistences.append(cycle_life_time)
                        if cycle_life_time > thresh:
                            if rep not in representatives:
                                representatives.append(rep)
                                cycle_2_info.append([cycle_life_time,birth,cycle_length,rep])
                            sum_lengths = sum_lengths + cycle_length
                            sum_cycles = sum_cycles + cycle_life_time
                        else:
                            sum_lengths = sum_lengths + cycle_length
                            sum_cycles = sum_cycles + cycle_life_time
                    k = k + 1
                h_2 = (1/cycle_count)*(sum_cycles/maximum_filtration_value)
                h_2_normalized = (1/cycle_count)*(sum_lengths/N)*(sum_cycles/maximum_filtration_value)
writeOutput()
outputLists(cycle_1_births,cycle_1_persistences,cycle_1_lengths,1,network)
outputLists(cycle_2_births,cycle_2_persistences,cycle_2_lengths,2,network)
