#!/usr/bin/env python

import argparse, sys, scipy, numpy, copy, subprocess

import lib
from lib import Lots, Event, get_parameters
from lxml import etree
from scipy import interpolate

from matplotlib import rc

rc('font',**{'family':'serif','serif':['Times'], 'size': 10})
rc('text', usetex=True)

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

parser = argparse.ArgumentParser(description='Simulate lots.')
parser.add_argument('output', type=str, default=None, help='Output file.')
parser.add_argument('lots', type=str, nargs='+', help='Lots to test in order.')
parser.add_argument('--count', type=int, default=10, help='Times to repeat each test.')
parser.add_argument('--verbose', action='store_true', default=False, help='enable verbose output')
parser.add_argument('--capacity', type=int, default=200,
                    help='Lot capacity. Should match lot description.')
args = parser.parse_args()

monitored_fractions = [0.01, 0.05, 0.1, 0.2, 0.5]

fig = plt.figure()
for index, lot in enumerate(args.lots):
  tree = etree.parse(lot)
  full_name = tree.xpath("//name")[0].get('value')
  lot_results = {}
  for monitored_fraction in monitored_fractions:
    for i in range(args.count):
      output = subprocess.check_output("./simulator.py %s %s 0.0 0.9 0.9 --seed=%d | ./capacity.py" % (lot, monitored_fraction, (index + 1)), shell=True)
      for line in output.split("\n"):
        if line.strip() == "":
          continue
        name, result = line.split(" ")
        if not lot_results.has_key(name):
          lot_results[name] = {}
        if not lot_results[name].has_key(monitored_fraction):
          lot_results[name][monitored_fraction] = []
        lot_results[name][monitored_fraction].append((abs(float(result) - (monitored_fraction * args.capacity)) / (monitored_fraction * args.capacity)) * 100.)
  ax = plt.subplot(1, len(args.lots), (index + 1))
  ax.set_title("\\textbf{%s}" % (full_name,))
  for lot in sorted(lot_results.keys()):
    X, Y, Yerr = [], [], []
    for monitored_fraction in sorted(lot_results[lot].keys()):
      X.append(monitored_fraction)
      Y.append(numpy.mean(lot_results[lot][monitored_fraction]))
      Yerr.append(numpy.std(lot_results[lot][monitored_fraction]))
    ax.errorbar(X, Y, xerr=Yerr, label='Lot %d' % (int(lot[-1])))
  if index == 0:
    ax.legend(loc='upper right', fontsize=8)
    ax.set_ylabel("\\textbf{Estimate Error}")
  ax.set_xlabel("\\textbf{Monitored Fraction}")

fig.set_size_inches(9.,2.5)
fig.tight_layout()
plt.savefig(args.output,bbox_inches='tight')
