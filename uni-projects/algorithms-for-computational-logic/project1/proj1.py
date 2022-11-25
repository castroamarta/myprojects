#!/usr/bin/env python
import sys
from sys import stdout
from subprocess import call

def MapVar(job, machine, timestep, n_jobs, n_machines, n_timesteps):

  return job + machine*n_jobs + timestep*n_jobs*n_machines + 1 

def MapVarInv(n, n_jobs, n_machines, n_timesteps):

  a ,r = ((n - 1)// (n_jobs*n_machines)), ((n - 1) % (n_jobs*n_machines)) 
  timestep = a
  machine, job = (r // n_jobs), (r % n_jobs)

  return [job, machine, timestep]

def lowerBound(m_time):

  srow = max([sum (i) for i in m_time])
  scol =max([sum([r[i] for r in m_time]) for i in range(0, len(m_time[0]))]) 

  return max(srow, scol) 

def print1(n_jobs, n_machines, n_timesteps, m_time):

  for job in range(n_jobs):
    for machine in range(n_machines):
      if m_time[job][machine] != 0 and machine != n_machines - 1:
        for m in range(machine + 1, n_machines):
          if m_time[job][m] != 0:
            for timestep in range(n_timesteps - m_time[job][machine] + 1):
              if m_time[job][machine] < m_time[job][m]:
                for t in range(n_timesteps - m_time[job][m] + 1): 
                  if t < m_time[job][machine] + timestep:
                   # print job, machine, timestep,' ', job, m ,t,' 0'
                    print >>f, -MapVar(job, machine, timestep, n_jobs, n_machines, n_timesteps),' ',-MapVar(job, m, t, n_jobs, n_machines, n_timesteps),' 0'
              else:
                for t in range(m_time[job][machine] + timestep):
                  # print job, machine, timestep,' ', job, m ,t,' 0'
                  print >>f, -MapVar(job, machine, timestep, n_jobs, n_machines, n_timesteps),' ',-MapVar(job, m, t, n_jobs, n_machines, n_timesteps), ' 0'

# In each timestep there is at most one task being executed [naive encoding] :)

def print2(n_jobs, n_machines, n_timesteps, m_time):

  for machine in range(n_machines):
    for job in range(n_jobs):
      if m_time[job][machine] != 0:
        for j in (range(job+1, n_jobs) + range(job)):
          if m_time[j][machine] != 0:
            for timestep in range(n_timesteps-m_time[job][machine] + 1):
              if (m_time[job][machine] + timestep) < (n_timesteps - m_time[j][machine] + 1):
                for t in range(timestep, m_time[job][machine] + timestep):
                  # print job, machine, timestep,' ',j ,machine, t,' 0'
                  print >>f,-MapVar(job, machine, timestep, n_jobs, n_machines, n_timesteps),' ',-MapVar(j ,machine, t, n_jobs, n_machines, n_timesteps),' 0'
              else:
                for t in range(timestep, n_timesteps - m_time[j][machine] + 1):          
                  # print job, machine, timestep,' ',j ,machine, t,' 0'
                  print >>f,-MapVar(job, machine, timestep, n_jobs, n_machines, n_timesteps),' ',-MapVar(j ,machine, t, n_jobs, n_machines, n_timesteps),' 0'

# Each task has to start at most in one timestep [naive encoding] :)

def print3(n_jobs, n_machines, n_timesteps, m_time):

  for job in range(n_jobs):
    for machine in range(n_machines):
      for timestep in range(n_timesteps-m_time[job][machine] + 1):
        for t in (range(timestep+1, n_timesteps-m_time[job][machine] + 1) + range(timestep)):
          # print job,machine,timestep,' ',job,machine,t
          print >>f, -MapVar(job,machine,timestep,n_jobs,n_machines,n_timesteps),' ',-MapVar(job,machine,t,n_jobs,n_machines,n_timesteps),' 0'
            

# Each task has to start at least in one timestep 

def print4(n_jobs, n_machines, n_timesteps, m_time):

  for job in range(n_jobs):
    for machine in range(n_machines):  
      if m_time[job][machine] != 0:
        for timestep in range(n_timesteps-m_time[job][machine]+1): 
          print >>f, MapVar(job, machine, timestep,n_jobs, n_machines, n_timesteps),' ',
        print >>f,'0'   

# main

# read input

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

# linear search for minimum timespan starting from the bottom

lines = ['UNSAT']
n_timesteps = lowerBound(m_time) 
n_var = 1
n_clauses = 1

while lines[0] != 'SAT':
  
  f = open("formula.cnf","w")

  print >>f, 'p cnf',n_var,n_clauses

  print1(n_jobs, n_machines, n_timesteps, m_time)
  print2(n_jobs, n_machines, n_timesteps, m_time)
  print3(n_jobs, n_machines, n_timesteps, m_time)
  print4(n_jobs, n_machines, n_timesteps, m_time)

  f.close()

  with open("resstd", "w") as of:
    with open("rerr", "w") as ef:
      call(["minisat","-verb=0","formula.cnf","resultado.txt"],stdout = of,stderr =ef)

  lines = [line.rstrip('\n') for line in open("resultado.txt","r")]
  n_timesteps = n_timesteps + 1

min_timespan = n_timesteps - 1

sol = []
for i in lines[1].split():
  	if int(i) >  0:
  		sol.append(MapVarInv(int(i),n_jobs,n_machines,n_timesteps))

l = []
for i in sol:
    l.append([int(i[0])+1,int(i[1])+1,i[2]])

srt_l = sorted(l)

# write output

printf = stdout.write

printf(str(min_timespan)+"\n")
printf (str(n_jobs)+ " " + str(n_machines)+"\n")

for k in range(1,n_jobs+1):
	printf(str(machines_per_job[k-1])+" ")
	for j in range(len(srt_l)):
	    if srt_l[j][0] == k:
	    	printf(str(srt_l[j][1])+":"+str(srt_l[j][2])+" ")
	printf ("\n")  

