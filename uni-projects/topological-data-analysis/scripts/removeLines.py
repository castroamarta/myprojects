#!/usr/bin/env python
# encoding=utf8
import sys

# Whenever the wrcf.py is stopped at step t for taking a long time, this script is used
# to retain only the information until step t - 1

def readFile(path_in):
    with open(path_in, "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [c.split() for c in content]
    return content

def outputNew(path_out):
    aux1 = []
    sys.stdout = open(path_out, 'w')
    filtration_value = 1295 # step t at which the script was stopped
    found = 0
    for line in lines:
        for l in line:
            if found == 0:
                aux = l.split(',')
                for elem in aux:
                    if elem == str(filtration_value)+");":
                        found = 1
        if found == 0:
            aux1.append(line)
    for line in aux1:
        for elem in line:
            sys.stdout.write(elem),
            sys.stdout.write(" "),
        sys.stdout.write("\n")
    sys.stdout.write("stream.finalizeStream();\n")
    sys.stdout.write("persistence = api.Plex4.getModularSimplicialAlgorithm(3, 2);\n")
    sys.stdout.write("intervals = persistence.computeAnnotatedIntervals(stream)\n")
    sys.stdout.write("options.filename = \'Barcode\';\n")
    sys.stdout.write("options.file_format = \'png\';\n")
    sys.stdout.write("options.max_filtration_value = "+str(filtration_value-1)+";\n")
    sys.stdout.write("plot_barcodes(intervals, options);\n")
    sys.stdout.write("diary off\n")

path_in = "/home/marta/WRCF/subject005/output005.m"
lines = []
lines = readFile(path_in)
path_out = "/home/marta/WRCF/subject005/new_output005.m"
outputNew(path_out)
