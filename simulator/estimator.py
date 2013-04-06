#!/usr/bin/env python

import argparse, sys

from lib import Estimation, Event, get_parameters
from lxml import etree

parser = argparse.ArgumentParser(description='Estimate lot availability.')
parser.add_argument('error', type=float, help='Relative error in monitored driver rate.')
parser.add_argument('search', type=float, help='Probability of searches in desirable lots.')
parser.add_argument('--interval', type=str, default='15M',
                    help='Interval in minutes for rate estimation. Default is 15 minutes.')
parser.add_argument('--seed', type=int, help='Random seed. Default is random seed.', default=None)
parser.add_argument('--verbose', action='store_true', default=False, help='enable verbose output')
args = parser.parse_args()

tree = get_parameters(sys.stdin)
estimation = Estimation(args, tree)

for line in sys.stdin:
  e = Event.loads(line.strip(), estimation.lots)
  if e == None:
    continue
  estimation.event(e)
