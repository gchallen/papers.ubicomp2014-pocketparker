#!/usr/bin/env python

import argparse, sys, scipy, numpy, copy

import lib
from lib import Lots, Event, get_parameters
from lxml import etree
from scipy import interpolate

from matplotlib import rc

rc('font',**{'family':'serif','serif':['Times'], 'size': 14})
rc('text', usetex=True)

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

parser = argparse.ArgumentParser(description='Simulate lots.')
parser.add_argument('--output', type=str, default=None, help='Output file.')
parser.add_argument('--verbose', action='store_true', default=False, help='enable verbose output')
parser.add_argument('--resample', type=int, default=60, help='Resample interval in sec. Default 60.')
args = parser.parse_args()

tree = get_parameters(sys.stdin)
lots = Lots(tree)

lot_counts = {}
time, max_time = 0., 0.

for lot in lots.lots:
  lot_counts[lot.name] = [(0., lot.count)]
for line in sys.stdin:
  e = Event.loads(line.strip(), lots)
  if e == None or not e.parked:
    continue
  if e.time > max_time:
    max_time = e.time
  if e.is_arrival:
    lot_counts[e.lot.name].append((e.time, lot_counts[e.lot.name][-1][1] + 1))
  else:
    lot_counts[e.lot.name].append((e.time, lot_counts[e.lot.name][-1][1] - 1))

if args.verbose:
  print >>sys.stderr, "Resampling counts"

resampled_counts = {}
for lot, counts in lot_counts.items():
  f = interpolate.interp1d([count[0] for count in counts],
                           [count[1] for count in counts])
  max_time = max([count[0] for count in counts])
  resampled_counts[lot] = zip(numpy.arange(0., max_time - 1., args.resample),
                              f(numpy.arange(0., max_time - 1., args.resample)))

"""
if args.verbose:
  print >>sys.stderr, "Filtering counts"

filtered_counts = {}
filter_window = []
for lot, counts in resampled_counts.items():
  filtered_counts[lot] = []
  for count in counts:
    filter_window.append(count[1])
    filter_window = filter_window[-1200:]
    filtered_counts[lot].append((count[0], count[1] - (float(sum(filter_window)) / len(filter_window))))
"""
filtered_counts = copy.copy(resampled_counts)

if args.verbose:
  print >>sys.stderr, "Binning counts"

binned_counts = {}
for lot, counts in filtered_counts.items():
  max_time = max([count[0] for count in counts])
  binned_counts[lot] = []
  for time in numpy.arange(0., max_time, 24. * 60. * 60.):
    binned = [count[1] for count in counts if count[0] > time and count[0] < time + 24. * 60. * 60.]
    binned_counts[lot].append(float(max(binned) - min(binned)))

for lot, counts in binned_counts.items():
  print "%s %.2f" % (lot, sum(counts) / len(counts))

if args.output != None:
  fig = plt.figure()
  ax = fig.add_subplot(111)
  plt.title("\\textbf{Monitored Capacity Estimation}")
  ax.set_xlabel("\\textbf{Day}")
  ax.set_ylabel("\\textbf{Running Count $a_l$}")
  for lot in lots.lots:
    lot_counts[lot.name] = [(t / 60. / 60. / 24., count) for t, count in lot_counts[lot.name]]
    ax.plot(*zip(*lot_counts[lot.name]), label="Lot %d" % (int(lot.name[-1]),))
  ax.legend(fontsize=10)
  plt.savefig(args.output,bbox_inches='tight')
