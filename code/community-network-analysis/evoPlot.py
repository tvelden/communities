# this script takes the quantitative summaries and make evolution plot
import glob
import numpy as np
import matplotlib.pyplot as plt

fileNames = glob.glob('*_summary.txt')
avgPaper = []
avgAu = []
avgDisper = []
for fileName in fileNames:
    f = open(fileName, 'rU')
    lines = f.readlines()
    f.close()
    avgPaper.append(float(lines[1].split(': ')[1]))
    avgAu.append(float(lines[2].split(': ')[1]))
    avgDisper.append(float(lines[3].split(': ')[1]))

linkStg = [sum(ls) for ls in zip(avgPaper, avgAu)]

plt.figure(figsize=(10, 8), dpi=500)
line1 = plt.plot(np.array(range(1995,2011)), np.array(avgPaper), label = 'Average # of Paper')
line2 = plt.plot(np.array(range(1995, 2011)), np.array(avgAu), label = 'Average # of People')
line3 = plt.plot(np.array(range(1995, 2011)), np.array(linkStg), label = 'Average Link Strength')
line4 = plt.plot(np.array(range(1995, 2011)), np.array(avgDisper), label = 'Average Dispersion')
plt.title('Evolution over 5 Year Sliding Windows', fontsize = 18)
plt.xlabel('5 Year Sliding Windows', fontsize = 15)
plt.ylabel('Average Number Underlying a Link', fontsize = 15)
plt.legend(loc = 'upper left')
plt.xlim(1995, 2010)
plt.grid()
plt.savefig('Evolution Average Number.png')

