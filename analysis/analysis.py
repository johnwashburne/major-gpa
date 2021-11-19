import numpy as np
import csv
import matplotlib.pyplot as plt

gpas = []
with open('results.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        gpas.append(float(row[1]))

x = np.array(gpas)
plt.hist(x, histtype='stepfilled', color='steelblue', edgecolor=None, bins=20, alpha=.50)
plt.show()
