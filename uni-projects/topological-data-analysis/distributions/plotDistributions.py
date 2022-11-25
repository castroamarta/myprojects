from __future__ import division
import matplotlib.pyplot as plt
import collections
import numpy as np

# Outputs the probability distributions

def readFile(path):
    with open(path, "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [c.split() for c in content]
    new_content = [[float(x) for x in lst] for lst in content]
    return content

def buildRegionsDistribution(content):
    new_content = []
    for elem in content:
        new = []
        for j in elem:
            e = j.split(",")
            for i in e:
                if i != "," or i != '\n':
                    if len(i) > 0:
                        new.append(int(i))
        a = list(set(new))
        new_content.append(a)

    new_count = []
    for l in new_content:
        count = [None]*116
        for i in range(116):
            if i in l:
                count[i] = 1
            else:
                count[i] = 0
        new_count.append(count)
    count = []
    for r in range(116):
        a = 0
        for l in new_count:
            a = a + l[r]
        count.append(a)

    x, y = [], []
    for i in range(116):
        x.append(i)
        y.append(count[i]/10)
    return x,y

def build_df(a):
    a_ord = sorted(a,reverse = True)
    a_cnt = collections.Counter(a_ord)
    a_cnt = a_cnt.most_common()
    new_cnt = []
    for elem in a_cnt:
        c = float(elem[0])
        new_cnt.append([c,elem[1]])
    new_cnt.sort(key = lambda x: (x[0],x[1]), reverse = False)
    x, y = [], []
    for elem in new_cnt:
        x.append(elem[0])
        y.append(elem[1]/len(a))
    return x,y

content = readFile("/home/marta/WRCF/distributions/persistences/subject010.txt")
a, b, c = content[0], content[1], content[2]

x_a,y_a = build_df(a)
x_b,y_b = build_df(b)
x_c,y_c = build_df(c)
#
fig, ax = plt.subplots()
plt.scatter(x_a, y_a, c='blue', marker = "o")
plt.plot(x_a, y_a,linewidth=1,c='blue')
plt.scatter(x_b, y_b, c='black', marker = "v",label = "Weight Reshuffle")
plt.plot(x_b, y_b,linestyle='dashed',linewidth=1,c='black')
plt.scatter(x_c, y_c, c='red', marker = "s",label = "Edge + Weight Reshuffle")
plt.plot(x_c, y_c,linestyle='dashed',linewidth=1,c='red')


plt.title("Persistence Distribution")

l1 = plt.Line2D([], [], color='blue', marker = "o", linestyle='None',
                          markersize=6, label="Data")
l2 = plt.Line2D([], [], color='black', marker="v", linestyle='None',
                          markersize=6, label="Weight Reshuffle")
l3 = plt.Line2D([], [], color='red', marker="s", linestyle='None',
                          markersize=6, label="Edge + Weight Reshuffle")


plt.legend(handles=[l1, l2, l3])
plt.xlim(0, 1)
# plt.xticks(np.arange(0, 115, step=5))
plt.ylim(0, 0.03)
plt.show()
