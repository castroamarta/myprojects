#!/usr/bin/python2.7
# File:  proj3.py
# Created on:  Sat, Nov 24, 2018 10:50:11
import sys
from sys import stdout
from subprocess import call

def lowerBound(m_time):

  srow = max([sum (i) for i in m_time])
  scol =max([sum([r[i] for r in m_time]) for i in range(0, len(m_time[0]))]) 

  return max(srow, scol)

def mapVar(job, machine, n_jobs):

  return job + machine*n_jobs + 1

def mapVarInv(n, n_jobs):

  machine ,job = ((n - 1)// n_jobs), ((n - 1) % (n_jobs)) 

  return [job, machine]  

def varNameA(job,machine,n_jobs):

    return "A"+str(mapVar(job,machine,n_jobs))
  #return "A"+str(job+1)+","+str(machine+1) 

def varNameI(job,machine,n_jobs):

    return "idx"+str(mapVar(job,machine,n_jobs))  
  # return "idx"+str(job+1)+","+str(machine+1)

def writeDataFile(f, n_jobs, n_machines, m_time):

    print >> f, "n_jobs = "+str(n_jobs)+";"
    print >> f, "n_machines = "+str(n_machines)+";"
    print >> f, "d = [|",
    for job in range(n_jobs):
        for machine in range(n_machines):
            if machine == n_machines-1 and job == n_jobs-1:
                print >> f, str(m_time[job][machine])+"|];"
            elif machine !=  n_machines-1: 
                print >> f, str(m_time[job][machine])+",",
            else: 
                print >> f, str(m_time[job][machine])+"|",

def variableDeclaration(f):

    print >> f, "set of int: I = 1..total;"
    print >> f, "int: n_jobs;"
    print >> f, "int: n_machines;"
    print >> f, "int: total = sum(i in 1..n_jobs, j in 1..n_machines) (d[i,j]);"
    print >> f, "array[1..n_jobs, 1..n_machines] of int: d;"

def buildBoolenArrays(f,n_jobs,n_machines, m_time):

    for job in range(n_jobs):
        for machine in range(n_machines):
            if m_time[job][machine] != 0:
                print >> f, "array[1..total] of var bool:"+str(varNameA(job, machine, n_jobs))+";"

def buildIndexArrays(f,n_jobs,n_machines, m_time):

    for job in range(n_jobs):
        for machine in range(n_machines):
            if m_time[job][machine] != 0:
                print >> f, "array[1..total] of var int:"+str(varNameI(job, machine, n_jobs))+";"    

def constraints(f,n_jobs, n_machines, m_time):
    
    # 1 - sequencia 
    for job in range(n_jobs):
        for machine in range(n_machines-1):             
            if m_time[job][machine] != 0:
                nextMachine = 0
                for m in range(machine + 1, n_machines):
                    if m_time[job][m] != 0 and nextMachine == 0:
                        nextMachine = 1

                        print >> f, "constraint forall(i in I where "+str(varNameA(job, 
                            machine, n_jobs))+"[i] == true) ("+str(varNameI(job, machine, n_jobs))+"[i] == i);"
                        print >> f, "constraint forall(i in I where "+str(varNameA(job, 
                            machine, n_jobs))+"[i] == false) ("+str(varNameI(job, machine, n_jobs))+"[i] == 0);"            
                        print >> f, "constraint forall(i in I where i <= max("+str(varNameI(job,
                            machine,n_jobs))+"))""("+str(varNameA(job, m, n_jobs))+"[i] == false);"
    
    
    # 2 - tarefas de jobs diferentes a correr no mesmo instante
    # 3 - uma tarefa tem que ser executada em d[i,j] unidades de tempo
    # 4 - a ultima tarefa de cada job tem qe ser executada antes do timespan
    for job in range(n_jobs):
        lastMachine = 0
        for machine in range(n_machines):
            if m_time[job][machine] != 0:
                lastMachine = machine
                print >> f, "constraint sum(bool2int("+str(varNameA(job, 
                    machine, n_jobs))+")) == d["+str(job + 1)+","+str(machine + 1)+"];"
            for j in range(n_jobs):
                if m_time[job][machine] != 0 and m_time[j][machine] != 0:
                    if j != job:
                        print >> f, "constraint forall(i in I) (not "+str(varNameA(job, 
                            machine, n_jobs))+"[i] \\/ not "+str(varNameA(j,machine,n_jobs))+"[i]);"       

        print >> f, "constraint forall(i in I where "+str(varNameA(job, lastMachine, n_jobs))+"[i] == true) ("+str(varNameI(job, lastMachine, n_jobs))+"[i] == i);"
        print >> f, "constraint forall(i in I where "+str(varNameA(job, lastMachine, n_jobs))+"[i] == false) ("+str(varNameI(job, lastMachine, n_jobs))+"[i] == 0);"
        print >> f, "constraint max("+str(varNameI(job, lastMachine, n_jobs))+") <= timespan;"


def writeOutput(f,n_jobs,n_machines):

    # timespan
    print >> f, "output[show(timespan)] ++ [\"\\n""\"];" 

    # conjunto de arrays com o valor 1 nos instantes ocupados por cada tarefa 
    firstMachine = 0
    print >> f, "output[",
    for job in range(n_jobs):
        for machine in range(n_machines):
            if m_time[job][machine] != 0:
                if firstMachine == 0:
                    print >> f, "\""+str(varNameA(job,machine,n_jobs)) +" = \",show(bool2int("+str(varNameA(job,machine,n_jobs))+")),"
                    firstMachine = 1
                else:
                    print >> f, "\"\\n"+str(varNameA(job,machine,n_jobs)) +" = \",show(bool2int("+str(varNameA(job,machine,n_jobs))+")),"                   
    print >> f, "];"    

def transformOutput(file):

    f  = open(file, "r")
    lines_aux = f.readlines()
    timespan = lines_aux[0].replace("\n", "")
    lines_aux.pop(0)
    lines=[]
    dic = {}
    for l in lines_aux:
        lines.append(l.split())

    for line in lines:
        key = line[0]
        executing = line[2:len(line)]
        duration = []
        start = False
        startPoint = -1
        for i in range(len(executing)):
            for char in list(executing[i]):
                if char.isdigit() and int(char) == 1:
                    if not start:
                        startPoint = i
                        start = True
                    if i == len(executing)-1:
                        duration.append([startPoint,i+1])
                elif char.isdigit() and int(char) == 0 and start:
                    duration.append([startPoint,i])
                    start = False
                    startPoint = -1

            dic[key] = duration
    
    return dic, timespan

def writeFinalOutput(dic, timespan):

    printf = stdout.write

    printf(str(timespan) + "\n")
    printf(str(n_jobs) + " " + str(n_machines) + "\n")

    lst = []

    for job in range(n_jobs):
        lst.append([None]*len(m_time[job]))

    for d in dic:
        newd = d.replace("A", "")
        jm = mapVarInv(int(newd), n_jobs)
        job = jm[0]
        machine = jm[1]
        lst[job][machine] = dic[d]

    for l in lst:
        machines = len(l)
        printf(str(machines) + " ")

        for m in range(machines):
            if l[m] != None:
                for duration in l[m]:
                    printf(str(m+1) + ":" + str(duration[0]) + ":" + str(duration[1] - duration[0]) + " ")

            if m == machines-1:
                printf("\n")        

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

# escreve ficheiro de dados .dzn
fdata = open("dados.dzn","w")

writeDataFile(fdata, n_jobs, n_machines, m_time)

fdata.close()

# escreve modelo .mzn
fmodel = open("model.mzn","w")

print >> fmodel,"var 1..total: timespan;"

variableDeclaration(fmodel)
buildBoolenArrays(fmodel,n_jobs,n_machines, m_time)
buildIndexArrays(fmodel,n_jobs,n_machines, m_time)
constraints(fmodel,n_jobs, n_machines, m_time)

print >> fmodel,"solve minimize timespan;"

writeOutput(fmodel,n_jobs,n_machines)

fmodel.close()

# chamada do minizinc
with open("arraySet.txt", "w") as of:
    call(["mzn-fzn","model.mzn","dados.dzn"],stdout = of) 

dic, timespan = transformOutput("arraySet.txt")
writeFinalOutput(dic, timespan)