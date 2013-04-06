#!/usr/bin/env python

import argparse, sys
from matplotlib import rc

rc('font',**{'family':'serif','serif':['Times'], 'size': 14})
rc('text', usetex=True)

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Simulate lots.')
parser.add_argument('output', type=str, default=None, help='Output file.')
parser.add_argument('rates', type=int, nargs='+', help='Rates to display.')
parser.add_argument('--capacity', type=int, default=200, help='Actual rate. Default is 200.')
args = parser.parse_args()

print args.rates
sys.exit()

fig = plt.figure()
ax = fig.add_subplot(111)
plt.title("\\textbf{Monitored Capacity Estimation}")
ax.set_xlabel("\\textbf{Day}")
ax.set_ylabel("\\textbf{Running Count $a_l$}")
for lot in lots.lots:
  lot_counts[lot.name] = [(t / 60. / 60. / 24., count) for t, count in lot_counts[lot.name]]
  ax.plot(*zip(*lot_counts[lot.name]), label="Lot %d" % (int(lot.name[-1]),))
ax.legend(fontsize=8)
plt.savefig(args.output,bbox_inches='tight')
