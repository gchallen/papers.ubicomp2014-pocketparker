#!/usr/bin/env python

import argparse, sys, scipy, numpy, copy, subprocess, re

import lib
from lib import Lots, Event, get_parameters
from lxml import etree
from scipy import interpolate

from matplotlib import rc

rc('font',**{'family':'serif','serif':['Times'], 'size': 12})
rc('text', usetex=True)

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

parser = argparse.ArgumentParser(description='Simulate lots.')
parser.add_argument('output', type=str, default=None, help='Output file.')
parser.add_argument('runs', type=str, nargs='+', help='Lots to test in order.')
parser.add_argument('--verbose', action='store_true', default=False, help='enable verbose output')
args = parser.parse_args()

capacity_pattern = re.compile(r"^(?P<time>[\d\.]+) C (?P<name>\w+) (?P<capacity>\d+).*")
probability_pattern = re.compile(r"^(?P<time>[\d\.]+) (?P<type>(?:P|P\*)) (?P<name>\w+) (?P<probability>[\d\.]+).*")

fig = plt.figure()
for index, run in enumerate(args.runs):
  capacities = {}
  probabilities = {}
  f = open(run, 'r')
  tree = get_parameters(f)
  for line in f:
    capacity_match = capacity_pattern.match(line)
    if capacity_match:
      time, name, capacity = float(capacity_match.group('time')), \
          capacity_match.group('name'), int(capacity_match.group('capacity'))
    else:
      probability_match = probability_pattern.match(line)
      if probability_match:
        time, type, name, probability = \
            float(probability_match.group('time')), probability_match.group('type'), \
            probability_match.group('name'), float(probability_match.group('probability'))
        print time, type, name, probability
