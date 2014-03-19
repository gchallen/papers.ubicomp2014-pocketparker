#!/usr/bin/env python

import argparse, sys, scipy, numpy, copy, subprocess, re

import lib
from lib import Lots, Event, get_parameters, HOURS_TO_SECONDS
from lxml import etree
from scipy import interpolate

from matplotlib import rc

rc('font',**{'family':'serif','serif':['Times'], 'size': 8})
rc('text', usetex=True)

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

parser = argparse.ArgumentParser(description='Simulate lots.')
parser.add_argument('output', type=str, default=None, help='Output file.')
parser.add_argument('run', type=str, help='Run to use.')
parser.add_argument('--verbose', action='store_true', default=False, help='enable verbose output')
args = parser.parse_args()

capacity_pattern = re.compile(r"^(?P<time>[\d\.]+) C (?P<name>\w+) (?P<capacity>\d+).*")
probability_pattern = re.compile(r"^(?P<time>[\d\.]+) (?P<type>(?:P|P\*)) (?P<name>\w+) (?P<probability>[\d\.]+).*")

capacities = {}
probabilities = {}
f = open(args.run, 'r')
tree = get_parameters(f)
run_name = tree.xpath("//name")[0].get('value')
for line in f:
  capacity_match = capacity_pattern.match(line)
  if capacity_match:
    time, name, capacity = (float(capacity_match.group('time')) / HOURS_TO_SECONDS), \
        capacity_match.group('name'), int(capacity_match.group('capacity'))
    if not capacities.has_key(name):
      capacities[name] = []
    capacities[name].append((time, capacity))
  else:
    probability_match = probability_pattern.match(line)
    if probability_match:
      time, type, name, probability = \
          (float(probability_match.group('time')) / HOURS_TO_SECONDS), probability_match.group('type'), \
          probability_match.group('name'), float(probability_match.group('probability'))
      if not probabilities.has_key(name):
        probabilities[name] = [(0., 1.)]
      probabilities[name].append((time, probability))
fig = plt.figure()
for i, lot in enumerate(capacities.keys()):
  probabilities[lot].append((24., 1.))
  ax1 = plt.subplot(1,len(capacities.keys()), (i + 1))
  ax1.plot(*zip(*(capacities[lot])), label='Lot Capacity')
  if i==0:
    ax1.legend(bbox_to_anchor=(1, 1.15), fontsize=6)
  #if i == 0:
 # ax1.set_title('\\textbf{Capacity v. Availability Probability: %s}' % (run_name,))
  #ax1.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
  #else:
  ax1.set_xlabel('\\textbf{Time}')
  if i==0:
    ax1.set_ylabel('\\textbf{Actual Capacity}')
  ax2 = ax1.twinx()
  ax2.plot(*zip(*(probabilities[lot])), label='Available Probability', color='black')
  ax2.axis(ymin=-0.5, ymax=1.5)
  if i==1:
    ax2.legend(bbox_to_anchor=(1, 1.15), fontsize=6)
    ax2.set_ylabel('\\textbf{Available Probability}')
  ticks = ax2.yaxis.get_ticklocs()
  ax2.yaxis.set_ticks([v for v in ticks if v >= 0. and v <= 1.])
fig.set_size_inches(3.5, 1.5)
plt.subplots_adjust(wspace=0.4)
plt.savefig(args.output,bbox_inches='tight')
