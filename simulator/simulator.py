#!/usr/bin/env python

import argparse, sys

from lib import Simulation, Lots, Rate, Event, print_parameters
from lxml import etree

parser = argparse.ArgumentParser(description='Simulate lots.')
parser.add_argument('lots', type=str, help='Lots XML file.')
parser.add_argument('monitored', type=float, help='Monitored driver rate.')
parser.add_argument('search', type=float, help='Labeled search rate.')
parser.add_argument('arrival', type=float, help='Arrival detection rate.')
parser.add_argument('departure', type=float, help='Departure detection rate.')
parser.add_argument('--seed', type=int, help='Random seed. Default is disabled.', default=None)
parser.add_argument('--repeat', type=int, help='Repeat count. Default is 7.', default=7)
parser.add_argument('--verbose', action='store_true', default=False, help='enable verbose output')
args = parser.parse_args()

simulation = Simulation(args)
tree = etree.parse(args.lots)
tree.getroot().append(simulation.to_xml())
lots = Lots(tree)
rates = Rate.from_tree(tree)

time = 0.

print_parameters(tree)

for count in range(args.repeat):
  for rate in rates:
    for event in rate.events(time):
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
          print event
        elif event.is_departure and simulation.saw_departure():
          print event
      print lots.print_capacity(event.time)
    time += rate.length
