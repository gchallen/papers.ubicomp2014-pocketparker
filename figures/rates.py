#!/usr/bin/env python

import argparse, sys, numpy
from matplotlib import rc
from scipy import misc

rc('font',**{'family':'serif','serif':['Times'], 'size': 14})
rc('text', usetex=True)

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Simulate lots.')
parser.add_argument('output', type=str, default=None, help='Output file.')
parser.add_argument('rates', type=int, nargs='+', help='Rates to display.')
parser.add_argument('--capacity', type=int, default=200, help='Actual rate. Default is 200.')
args = parser.parse_args()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.title("\\textbf{Rate Estimation}")
ax.set_xlabel("\\textbf{Scaled Rate}")
ax.set_ylabel("\\textbf{Probability}")

for rate in args.rates:
  probs = []
  monitored = (float(rate) / args.capacity)
  prob_sum = 0.
  for i in numpy.arange(rate, args.capacity * 2, 1):
    prob = misc.comb([i], [rate])[0] * (monitored ** rate) * ((1. - monitored) ** (i - rate))
    prob_sum += prob
    probs.append((i, prob))
  probs = [(i, prob / prob_sum) for i, prob in probs]
  ax.plot(*zip(*probs), label="%d Observed, %.2f Monitored Fraction" % (rate, monitored,))

ax.legend(fontsize=10)
plt.savefig(args.output,bbox_inches='tight')
