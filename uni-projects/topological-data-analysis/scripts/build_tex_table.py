import sys

def readFile(path):
    with open(path, "r") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    content = [c.split() for c in content]
    # new_content = [[float(x) for x in lst] for lst in content]
    return content

path = "/home/marta/WRCF/labels.txt"
content = readFile(path)
new = content[1:]

path_out = '/home/marta/WRCF/tex_table.txt'
sys.stdout = open(path_out, 'w')
sys.stdout.write('\\begin{table}[h!]')
sys.stdout.write('\n\\footnotesize')
sys.stdout.write('\n\\renewcommand{\\arraystretch}{1.7}')
sys.stdout.write('\n\\centering')
sys.stdout.write('\n\\begin{tabular}{| m{5em} || m{50em} |}')
sys.stdout.write('\n\\hline ')
sys.stdout.write('\nID & Region\\\\')
for elem in new:
    new_s = []
    for s in elem[1]:
        if s == '_':
            new_s.append('\\_')
        else:
            new_s.append(s)
    print "\n$"+str(elem[0])+"$ & ",
    for i in new_s:
        sys.stdout.write(str(i))
    sys.stdout.write(' \\\\')
sys.stdout.write('\n\\hline\\hline')
sys.stdout.write('\n\\end{tabular}')
sys.stdout.write('\n\\caption{llllnetwork.}')
sys.stdout.write('\n\\label{table:1}')
sys.stdout.write('\n\\end{table}')
sys.stdout.close()
