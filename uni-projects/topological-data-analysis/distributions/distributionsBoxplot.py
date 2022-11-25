import matplotlib.pyplot as plt
import numpy as np

# Outputs boxplots comparing distributions

def readFile(path):
    with open(path, "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [c.split() for c in content]
    new_content = [[float(x) for x in lst] for lst in content]
    return new_content

data_a = readFile("/home/marta/WRCF/distributions/persistences/comparisons/all_persistences_original.txt")

data_b = readFile("/home/marta/WRCF/distributions/persistences/comparisons/all_persistences_w_r.txt")

data_c = readFile("/home/marta/WRCF/distributions/persistences/comparisons/all_persistences_e_w_r.txt")

ticks = ['Subject 1', 'Subject 2', 'Subject 3','Subject 4', 'Subject 5', 'Subject 6','Subject 9','Subject 10', 'Subject 14', 'Subject 15']

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color='#000000')


plt.figure()

bpl = plt.boxplot(data_a, positions=np.array(xrange(len(data_a)))*2.0-0.6, sym='', widths=0.35,patch_artist=True)
bpr = plt.boxplot(data_b, positions=np.array(xrange(len(data_b)))*2.0, sym='', widths=0.35,patch_artist=True)
bpq = plt.boxplot(data_c, positions=np.array(xrange(len(data_c)))*2.0+0.6, sym='', widths=0.35,  patch_artist=True)
set_box_color(bpl, '#8c6bb1')
set_box_color(bpr, '#9ebcda')
set_box_color(bpq, '#fdd0a2')


plt.plot([], c='#8c6bb1', label='Original')
plt.plot([], c='#9ebcda', label='Weight Reshuffle')
plt.plot([], c='#fdd0a2', label='Edge-Weight Reshuffle')
plt.legend()

plt.title('Persistence Distribution Comparision')
plt.xticks(xrange(0, len(ticks) * 2, 2), ticks, rotation = 60)
plt.xlim(-2, len(ticks)*2)
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig('all_groups_persistence1.png')
