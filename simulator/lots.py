#!/usr/bin/env python

import argparse, sys, scipy, numpy, copy

from lib import Simulation, Lots, Rate, Event, print_parameters, HOURS_TO_SECONDS
from lxml import etree

from matplotlib import rc

rc('font',**{'family':'serif','serif':['Times'], 'size': 10})
rc('text', usetex=True)

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Produce lot plots.')
parser.add_argument('output', type=str, default=None, help='Output file.')
parser.add_argument('lots', type=str, nargs='+', help='Lots to graph in order.')
parser.add_argument('--seed', type=int, help='Random seed. Default 1.', default=1)
parser.add_argument('--verbose', action='store_true', default=False, help='enable verbose output')
args = parser.parse_args()

class FakeArgs(object):
  def __init__(self, seed):
    self.seed = seed
    self.monitored = 1.
    self.search = 0.
    self.arrival = 1.
    self.departure = 1.

fig = plt.figure()

for i, lot in enumerate(args.lots):

  fake_args = FakeArgs(args.seed)
  simulation = Simulation(fake_args)
  tree = etree.parse(lot)
  name = tree.xpath("//name")[0].get('value')
  lots = Lots(tree)
  rates = Rate.from_tree(tree)

  time = 0.
  arrivals = []
  departures = []
  capacities = {}
  for lot in lots.lots:
    capacities[lot] = [(0., lot.count)]
  for rate in rates:
    arrivals.append((time / HOURS_TO_SECONDS, rate.arrival * HOURS_TO_SECONDS))
    arrivals.append(((time + rate.length) / HOURS_TO_SECONDS, rate.arrival * HOURS_TO_SECONDS))
    departures.append((time / HOURS_TO_SECONDS, -1 * rate.departure * HOURS_TO_SECONDS))
    departures.append(((time + rate.length) / HOURS_TO_SECONDS, -1 * rate.departure * HOURS_TO_SECONDS))
    for event in rate.events(time):
      for lot in lots.lots:
        capacities[lot].append((event.time / HOURS_TO_SECONDS, lot.count))
      if event.is_arrival:
        event = lots.park(event)
      elif event.is_departure:
        event = lots.leave(event)
      else:
        raise Exception("Problem with event type")
      event.saw_search = simulation.saw_search()
      if event.time < time:
        raise Exception(event.time, time)
      if event.parked and simulation.saw_driver():
        if event.is_arrival and simulation.saw_arrival():
          pass
        elif event.is_departure and simulation.saw_departure():
          pass
    time += rate.length
  ax1 = plt.subplot(2, len(args.lots), (i + 1))
  ax1.set_title("\\textbf{%s}" % (name,))
  for lot in lots.lots:
    ax1.plot(*zip(*(capacities[lot])), label='Lot %d' % (int(lot.name[-1]),))
  if i == 0:
    ax1.set_ylabel("\\textbf{Capacity}")
  ax1.axis(xmin=0, xmax=24, ymin=0, ymax=max([lot.capacity for lot in lots.lots]))
  if i == 0:
    ax1.legend(loc='upper right', fontsize=8)
  ax2 = plt.subplot(2, len(args.lots), (i + len(args.lots) + 1))
  ax2.plot(*zip(*arrivals), label='Arrival', color='blue')
  ax2.fill_between(*zip(*arrivals), color='blue')
  ax2.plot(*zip(*departures), label='Departure', color='green')
  ax2.fill_between(*zip(*departures), color='green')
  if i == 0:
    ax2.set_ylabel("\\textbf{Rate}")
  ax2.set_xlabel("\\textbf{Hour}")
  ax2.axis(xmin=0, xmax=24,
           ymin=min([rate for t, rate in departures]),
           ymax=max([rate for t, rate in arrivals]))
  if i == 0:
    ax2.legend(loc='upper right', fontsize=8)

fig.set_size_inches(9.,4.)
fig.tight_layout()
plt.savefig(args.output,bbox_inches='tight')
