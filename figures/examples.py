#!/usr/bin/env python

import argparse, sys, numpy
import matplotlib.mlab as mlab
from matplotlib import rc
from scipy import misc

rc('font',**{'family':'serif','serif':['Times'], 'size': 16})
rc('text', usetex=True)

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Generate example lot shifts.')
parser.add_argument('--capacity', type=int, default=100, help='Capacity of lot. Default is 100.')
parser.add_argument('--start', type=int, default=70, help='Mean before shift. Default is 30 from the relevant border.')
parser.add_argument('--variance', type=int, default=20, help='Variance before shift. Default is 20.')
parser.add_argument('--shift', type=int, default=5, help='Arrival and departure shift width. Default is 5.')
parser.add_argument('--search', type=int, default=10, help='Search shift width. Default is 10.')
args = parser.parse_args()

def renormalize(probs):
  prob_sum = sum([v for v in probs.values() if not v == None])
  for count, prob in probs.items():
    if probs[count] == None:
      continue
    probs[count] /= prob_sum
  return probs

def to_array(probs):
  cs, ps = [], []
  for count in sorted(probs.keys()):
    if probs[count] == None:
      continue
    cs.append(count)
    ps.append(probs[count])
  return cs, ps

fig = plt.figure()

ax1 = plt.subplot(211)
ax1.set_title("\\textbf{Effect of Arrival}")
ax1.set_ylabel("\\textbf{Probability}")

probs = {}
for x in numpy.arange(0, args.capacity + 1, 1):
  probs[x] = mlab.normpdf(x, args.capacity - args.start, args.variance)
probs = renormalize(probs)
cs, ps = to_array(probs)

ax1.plot(cs, ps, label="Before", color='blue')
ax1.fill_between(cs, ps, 0, color='blue')
ax1.legend(loc='upper right')

for count, prob in probs.items():
  if count < args.shift:
    probs[count] = 0

probs = renormalize(probs)
for x in numpy.arange(0, args.capacity + 1, 1):
  if x > (args.capacity - args.shift):
    probs[x] = 0.
  else:
    probs[x] = probs[x + args.shift]
probs = renormalize(probs)
cs, ps = to_array(probs)

ax2 = plt.subplot(212, sharex=ax1)
ax2.plot(cs, ps, label="After", color='red')
ax2.fill_between(cs, ps, 0, color='red')
ax2.legend(loc='upper right')

ax2.set_ylabel("\\textbf{Probability}")
ax2.set_xlabel("\\textbf{Available Spots}")

plt.savefig('arrival.pdf',bbox_inches='tight')

##

fig = plt.figure()

ax1 = plt.subplot(211)
ax1.set_title("\\textbf{Effect of Departure}")

probs = {}
for x in numpy.arange(0, args.capacity + 1, 1):
  probs[x] = mlab.normpdf(x, args.capacity - args.start, args.variance)
probs = renormalize(probs)
cs, ps = to_array(probs)

ax1.plot(cs, ps, label="Before", color='blue')
ax1.fill_between(cs, ps, 0, color='blue')
ax1.legend(loc='upper right')

for x in numpy.arange(args.capacity, -1, -1):
  if x  < args.shift:
    probs[x] = None
  else:
    probs[x] = probs[x - args.shift]
probs = renormalize(probs)
cs, ps = to_array(probs)

ax2 = plt.subplot(212, sharex=ax1)
ax2.plot(cs, ps, label="After", color='red')
ax2.fill_between(cs, ps, 0, color='red')
ax2.legend(loc='upper right')

ax2.set_xlabel("\\textbf{Available Spots}")

plt.savefig('departure.pdf', bbox_inches='tight')

##

fig = plt.figure()

ax1 = plt.subplot(211)
ax1.set_title("\\textbf{Effect of Search}")

probs = {}
for x in numpy.arange(0, args.capacity + 1, 1):
  probs[x] = mlab.normpdf(x, args.capacity - args.start, args.variance)
probs = renormalize(probs)
cs, ps = to_array(probs)

ax1.plot(cs, ps, label="Before", color='blue')
ax1.fill_between(cs, ps, 0, color='blue')
ax1.legend(loc='upper right')
ax1.axis(ymin=0, ymax=0.1)

probs[0] = sum([prob for count, prob in probs.items() if count < args.search])

for x in numpy.arange(1, args.capacity + 1, 1):
  if x > (args.capacity - args.search):
    probs[x] = None
  else:
    probs[x] = probs[x + args.search]
probs = renormalize(probs)
cs, ps = to_array(probs)

ax2 = plt.subplot(212, sharex=ax1)
ax2.plot(cs, ps, label="After", color='red')
ax2.fill_between(cs, ps, 0, color='red')
ax2.legend(loc='upper right')
ax2.axis(ymin=0, ymax=0.1)

ax2.set_xlabel("\\textbf{Available Spots}")

plt.savefig('search.pdf', bbox_inches='tight')
