#!/usr/bin/env python
import sys
from sys import stdout
from subprocess import call
import re

def lowerBound(m_time):

  srow = max([sum (i) for i in m_time])
  scol =max([sum([r[i] for r in m_time]) for i in range(0, len(m_time[0]))]) 

  return max(srow, scol)

def transformInput():

	c = [line.strip() for line in sys.stdin]

	lst = []

	[lst.append(j) for j in [i.split(' ') for i in c]]

	machines_per_job = []

	[machines_per_job.append(int(lst[1:][i][0])) for i in range(len(lst)-1)]

	n_jobs, n_machines = int(lst[0][0]), int(lst[0][1]) 

	m_time = [[0 for j in range(n_machines)] for i in range(n_jobs)]

	ix = 0
	for t in lst[1:]:
		for q in t[1:]:
			m_time[ix][int(q.split(':')[0])-1] = int(q.split(':')[1])
		ix += 1 

	return m_time, n_jobs, n_machines

def writeAtoms(f, m_time, n_jobs, n_machines, timespan):

	print >> f, "step("+str(0)+"..timespan)."
	print >> f, "job("+str(1)+".."+str(n_jobs)+")."
	print >> f, "task("+str(1)+".."+str(n_machines)+")."

	for job in range(0,n_jobs):
		for machine in range(0,n_machines):
			if m_time[job][machine] != 0:
				print >> f, "valid("+str(job+1)+","+str(machine+1)+")."

def writeRules(f, m_time, n_jobs, n_machines, timespan):

	#1 - each task starts only once
	print >> f, str(1) + " {started(J,T,S): step(S)} " + str(1) + " :- job(J), task(T), valid(J,T).\n"

	#2 - init if started
	print >> f, "init(J,T) :- started(J,T,S).\n"

	#3 - each task has to run exactly the numr of steps of its duration
	for job in range(0,n_jobs):
		for machine in range(0,n_machines):
			if m_time[job][machine] != 0:
				print >> f, str(m_time[job][machine])+" {running("+str(job+1)+","+str(machine+1)+",S) : step(S)} "+ str(m_time[job][machine])+":- init("+str(job + 1)+","+str(machine + 1)+")."

	print >> f, "\n"

	#4 - evaluate to false if a task is running after timespan
	print >> f, ":- running(J,T,S), S >= timespan.\n"

	#5 - is running if has started
	print >> f, "running(J,T,S) :- started(J,T,S).\n"

	#6 - evaluate to false if a task is running before it has started.
	print >> f, ":- running(J,T,S), started(J,T,S1), S1 > S.\n"

	#7 - evaluate to false if any task T+1 is running before task T
	print >> f, ":- running(J,T,S), running(J,T1,S1), task(T1), T1 > T, step(S1), S1 <= S.\n"

	#8 - evaluate to false if two tasks of different jobs are running in the same step
	print >> f, ":- running(J,T,S), running(J1,T,S), J1 != J, job(J1).\n"

	#9 - print running predicate
	print >> f, "#show running/3."

def transformOutput(file):

	f  = open(file, "r")
	lines_aux = f.readlines()
	lines_aux = lines_aux[0].split()
	results = []
	lst = []
	dic = {}

	for l in lines_aux:
		results.append(re.findall(r'\d+', l))

	for job in range(n_jobs):
		lst.append([None]*len(m_time[job]))

	job = -1
	task = -1

	for result in results:

		if (int(result[0]) != job) or (int(result[1]) != task):

			if (job != -1):
				lst[job-1][task-1] = executing

			job = int(result[0])
			task = int(result[1])
			executing = [0] * timespan

		time = int(result[2])
		executing[time] = 1

	lst[job-1][task-1] = executing

	for j in range(n_jobs):

		for t in range(n_machines):

			duration = []
			start = False
			startPoint = -1
			executing = lst[j-1][t-1]

			if executing != None:

				for e in range(len(executing)):

					if executing[e] == 1:
						if not start:
							startPoint = e
							start = True
						if e == len(executing)-1:
							duration.append([startPoint,e+1])
					elif executing[e] == 0 and start:
						duration.append([startPoint,e])
						start = False
						startPoint = -1

				lst[j-1][t-1] = duration
	
	return lst

def writeFinalOutput(lst):

	printf = stdout.write

	printf(str(timespan) + "\n")
	printf(str(n_jobs) + " " + str(n_machines) + "\n")

	for l in lst:
		machines = len(l)
		printf(str(machines) + " ")

		for m in range(machines):
			if l[m] != None:
				for duration in l[m]:
					printf(str(m+1) + ":" + str(duration[0]) + ":" + str(duration[1] - duration[0]) + " ")

			if m == machines-1:
				printf("\n")


m_time, n_jobs, n_machines = transformInput()

timespan = lowerBound(m_time)

lines = ['UNSATISFIABLE']

while lines[0][0][0] != 'r':

	frules = open("jspi.lp","w")

	print >> frules, "#const timespan = "+str(timespan)+"."

	writeAtoms(frules, m_time, n_jobs, n_machines, timespan)
	writeRules(frules, m_time, n_jobs, n_machines, timespan)

	frules.close()

	# call clingo
	with open("result.txt", "w") as of:
	    call(["clingo","--verbose=0","jspi.lp"],stdout = of) 

	lines = [line.split(' ') for line in open("result.txt","r")]

	timespan = timespan + 1

timespan = timespan - 1

lst = transformOutput("result.txt")

writeFinalOutput(lst)