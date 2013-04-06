#!/usr/bin/env python

import argparse, sys, re, numpy

parser = argparse.ArgumentParser(description='Merge real lot data.')
parser.add_argument('events', type=str, help='File with events.')
parser.add_argument('l1', type=str, help='Lot capacities for L1.')
parser.add_argument('l2', type=str, help='Lot capacities for L2.')
args = parser.parse_args()

everything = []

L1 = 268
L2 = 344

for line in open(args.events, 'r'):
  time, type, lot, other = line.split()
  if lot == 'F':
    lot = 'L1'
  elif lot == 'J':
    lot = 'L2'
  everything.append((time, "%.2f %s %s" % (float(time), type, lot,)))

first = False
for line in open(args.l1, 'r'):
  time, count, unused, unused = line.split()
  if not first:
    for time in numpy.arange(0, int(time), 600):
      everything.append((time, "%.2f C P1 0" % (time,)))
    first = True
  everything.append((time, "%.2f C P1 %d" % (float(time), L1 - int(count))))

first = False
for line in open(args.l2, 'r'):
  time, count, unused, unused = line.split()
  if not first:
    for time in numpy.arange(0, int(time), 600):
      everything.append((time, "%.2f C P2 0" % (time,)))
    first = True
  everything.append((time, "%.2f C P2 %d" % (float(time), L1 - int(count))))

print """<root>
  <name value="Campus"/>
  <lot name="L1" capacity="268" count="0" weight="0.9" poi="A" order="1"/>
  <lot name="L2" capacity="344" count="0" weight="0.1" poi="A" order="2"/>
  <simulation monitored="0.10" search="0.0" arrival="0.9" departure="0.9" seed="5"/>
</root>"""
print "--------------------------"

everything = sorted(everything, key=lambda e: e[0])
for e in everything:
  print e[1]
