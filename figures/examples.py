#!/usr/bin/env python

import argparse, sys, numpy
import matplotlib.mlab as mlab
from matplotlib import rc
from scipy import misc

rc('font',**{'family':'serif','serif':['Times'], 'size': 14})
rc('text', usetex=True)

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Simulate lots.')
parser.add_argument('output', type=str, default=None, help='Output file.')
parser.add_argument('--capacity', type=int, default=100, help='Capacity of lot. Default is 100.')
parser.add_argument('--start', type=int, default=70, help='Mean before shift. Default is 30 from the relevant border.')
parser.add_argument('--variance', type=int, default=20, help='Variance before shift. Default is 20.')
parser.add_argument('--shift', type=int, default=5, help='Shift width. Default is 5.')
args = parser.parse_args()

def renormalize(probs):
  prob_sum = sum(probs.values())
  for count, prob in probs.items():
    probs[count] /= prob_sum
  return probs

def to_array(probs):
  array = []
  for count in sorted(probs.keys()):
    array.append((count, probs[count]))
  return array

fig = plt.figure()
plt.title("\\textbf{Effect of Arrival}")

ax1 = plt.subplot(211)
ax1.set_ylabel("\\textbf{Probability}")

probs = {}
for x in numpy.arange(0, args.capacity + 1, 1):
  probs[x] = mlab.normpdf(x, args.capacity - args.start, args.variance)
probs = renormalize(probs)

ax1.plot(*zip(*(to_array(probs))), label="Before")

ax2 = plt.subplot(212, sharex=ax1)
ax2.plot(*zip(*(to_array(probs))), label="Before")

ax2.set_xlabel("\\textbf{Available Spots}")

plt.savefig(args.output,bbox_inches='tight')
