#!/usr/bin/env python
import sys
from sys import stdout
from subprocess import call

def lowerBound(m_time):

  srow = max([sum (i) for i in m_time])
  scol =max([sum([r[i] for r in m_time]) for i in range(0, len(m_time[0]))]) 

  return max(srow, scol)

def MapVar(job, machine, n_jobs):

  return job + machine*n_jobs + 1

def MapVarInv(n, n_jobs):

  machine ,job = ((n - 1)// n_jobs), ((n - 1) % (n_jobs)) 

  return [job, machine]  

def varName(job,machine,n_jobs):

  return "t"+str(MapVar(job,machine,n_jobs))

def declareConst(n_jobs,n_machines):

  for job in range(n_jobs):
    for machine in range(n_machines):
      if m_time[job][machine] != 0:
        print >>f,"(declare-const",varName(job,machine,n_jobs),"Int)" 

def constraints(n_jobs,n_machines):
  
  print >>f,"(assert(and "
  for job in range(n_jobs):
    lastMachine = None
    for machine in range(n_machines):

      if (machine == 0) or (lastMachine == None):
        if m_time[job][machine] != 0:
          print >>f, "(>=",varName(job,machine,n_jobs),str(0),")"
          lastMachine = machine

      elif machine == n_machines - 1:
        if m_time[job][machine] != 0:
          print >>f, "(>=",varName(job,machine,n_jobs),"(+",varName(job,lastMachine,n_jobs),m_time[job][lastMachine],"))"
          print >>f, "(<= (+",varName(job,machine,n_jobs),m_time[job][machine],")",str(min_timespan),")"
          lastMachine = machine
        else:
          print >>f, "(<= (+",varName(job,lastMachine,n_jobs),m_time[job][lastMachine],")",str(min_timespan),")"

      else:
        if m_time[job][machine] != 0:
          print >>f, "(>=",varName(job,machine,n_jobs),"(+",varName(job,lastMachine,n_jobs),m_time[job][lastMachine],"))"
          lastMachine = machine

  for machine in range(n_machines):
    for job in range(n_jobs):
      for j in range(job+1,n_jobs):
        if (m_time[job][machine] != 0) and (m_time[j][machine] != 0):
          print >>f,"(or (>=",varName(job,machine,n_jobs),"(+",varName(j,
            machine,n_jobs),m_time[j][machine],")) (>=",varName(j,machine,n_jobs),"(+ ",varName(job,
            machine,n_jobs),m_time[job][machine],")))"
  
  print >>f,"))"


# main

# le o input

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

# procura linear do menor intervalo de tempo

lines = ['unsat']
min_timespan = lowerBound(m_time)

while lines[:1][0] != 'sat':
  
  f = open("formula.smt","w")

  declareConst(n_jobs,n_machines)
  constraints(n_jobs,n_machines)

  print >>f,"(check-sat)"
  print >>f,"(get-model)"

  f.close()

  with open("model.txt", "w") as of:
    call(["z3","-smt2","formula.smt"],stdout = of) 

  lines = [line.rstrip('\n') for line in open("model.txt","r")]
    
  min_timespan = min_timespan + 1

min_timespan = min_timespan - 1  

# le modelo em model.txt e coloca em mx

l = []
var, valor = -1, -1
for i in  range(len(lines[2:])-1):

  if i % 2 == 0:

    var =  lines[2:][i].split(' ')[3]

  else:

    valor = lines[2:][i].split(' ')[4].split(')')[0]

  if (var != -1) and (valor != -1):

    l.append([var,int(valor)])
    var = -1
    valor = -1

mx = [[0 for j in range(n_machines)] for i in range(n_jobs)]

for i in l:
  x , y = int(MapVarInv(int(i[0][1:]),n_jobs)[0]), int(MapVarInv(int(i[0][1:]),n_jobs)[1])
  if m_time[x][y] != 0:
    mx[x][y] = int(i[1])

# # # escreve o output

printf = stdout.write

printf(str(min_timespan)+"\n")
printf (str(n_jobs)+ " " + str(n_machines)+"\n") 
for j in range(n_jobs):
  printf (str(machines_per_job[j])+" ")
  for m in range(n_machines):
    if m_time[j][m]!= 0:
      printf( str(m+1)+":"+str(mx[j][m])+" ")
  printf("\n")  