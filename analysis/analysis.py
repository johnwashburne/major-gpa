import numpy as np
import csv
import matplotlib.pyplot as plt

gpas = []
table = []
with open('results_sorted.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        gpas.append(float(row[1]))
        table.append([row[0], row[1]])

x = np.array(gpas)
plt.hist(x, histtype='stepfilled', color='steelblue', edgecolor=None, bins=15, alpha=.50)
plt.xlabel("Grade Point Average")
plt.ylabel("Count")
plt.show()

print("Major Program | Average GPA")
print("---- | ----")

for row in table:
    program = row[0]
    program = program.replace("Bachelor of Science in ", "")
    program = program.replace("Bachelor of", "")
    print(program, "|", round(float(row[1]), 3))
