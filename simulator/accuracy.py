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
parser.add_argument('runs', type=str, nargs='+', help='Runs to use.')
parser.add_argument('--tie', type=float, default=0.01, help='Lot tie threshold. Default 0.01.')
parser.add_argument('--verbose', action='store_true', default=False, help='enable verbose output')
args = parser.parse_args()

capacity_pattern = re.compile(r"^(?P<time>[\d\.]+) C (?P<name>\w+) (?P<capacity>\d+).*")
probability_pattern = re.compile(r"^(?P<time>[\d\.]+) (?P<type>(?:P|P\*)) (?P<name>\w+) (?P<probability>[\d\.]+).*")
  
def best_lot(lots, capacities):
  available_lots = [lot for lot in lots if capacities[lot.name][-1][1] < lot.capacity]
  if len(available_lots) == 0:
    return None, None
  available_lots = sorted(available_lots, key=lambda l: l.order)
  return available_lots[0].name, available_lots[0].order

def estimated_best(lots, probabilities):
  sorted_lots = sorted(lots, key=lambda l: probabilities[l.name][-1][1], reverse=True)
  if len(sorted_lots) < 2:
    raise Exception
  if abs(probabilities[sorted_lots[0].name][-1][1] - probabilities[sorted_lots[1].name][-1][1]) < args.tie:
    return_lot = sorted(sorted_lots[0:2], key=lambda l: l.order)[0]
    return return_lot.name, return_lot.order
  else:
    return sorted_lots[0].name, sorted_lots[0].order

table_lines = {}
for run in args.runs:
  f = open(run, 'r')
  tree = get_parameters(f)
  lots = Lots(tree)
  run_name = tree.xpath("//name")[0].get('value')
  monitored = float(tree.xpath("//simulation")[0].get('monitored'))
  error = float(tree.xpath("//estimation")[0].get('error'))

  capacities = {}
  probabilities = {}

  for lot in lots.lots:
    capacities[lot.name] = [(0., lot.capacity)]
    probabilities[lot.name] = [(0., 0.)]

  total, correct, missed, wasted = 0, 0, 0, 0

  for line in f:
    capacity_match = capacity_pattern.match(line)
    if capacity_match:
      time, name, capacity = (float(capacity_match.group('time')) / HOURS_TO_SECONDS), \
          capacity_match.group('name'), int(capacity_match.group('capacity'))
      capacities[name].append((time, capacity))
    else:
      probability_match = probability_pattern.match(line)
      if probability_match:
        time, type, name, probability = \
            (float(probability_match.group('time')) / HOURS_TO_SECONDS), probability_match.group('type'), \
            probability_match.group('name'), float(probability_match.group('probability'))
        probabilities[name].append((time, probability))
    best_l, best_o = best_lot(lots.lots, capacities)
    estimated_l, estimated_o = estimated_best(lots.lots, probabilities)
    if best_l != None:
      if best_l == estimated_l:
        correct += 1
      elif best_o < estimated_o:
        missed += 1
      else:
        wasted += 1
      total += 1
  
  if not table_lines.has_key(run_name):
    table_lines[run_name] = {}
  if not table_lines[run_name].has_key(monitored):
    table_lines[run_name][monitored] = {}

  table_lines[run_name][monitored][error] = (total, correct, missed, wasted)

print r"""\begin{table}[t!]
\begin{threeparttable}
{\small
\begin{tabularx}{\columnwidth}{Xrrrrr}
\multicolumn{1}{c}{\textbf{Type}} & 
\multicolumn{1}{c}{\textbf{$f_m$}} & 
\multicolumn{1}{c}{\textbf{Correct}} & 
\multicolumn{1}{c}{\textbf{Missed}} & 
\multicolumn{1}{c}{\textbf{Waste}}\\ \toprule
"""

for run_name in sorted(table_lines.keys()):
  if not run_name == 'Campus':
      continue
#  print r"""\textbf{%s} & & & & & \\""" % (run_name,)
  first = True
  for monitored in sorted(table_lines[run_name]):
    for error in sorted(table_lines[run_name][monitored]):
      total, correct, missed, wasted = table_lines[run_name][monitored][error]
      if first:
        print r"""\textbf{%s} & %.2f & %.1f \%% & %.1f \%% & %.1f \%% \\""" % (run_name, monitored,
                                                           (float(correct) / total) * 100.,
                                                           (float(missed) / total) * 100.,
                                                           (float(wasted) / total) * 100.)
        first = False
      else:
        print r"""& %.2f & %.1f \%% & %.1f \%% & %.1f \%% \\""" % (monitored,
                                                           (float(correct) / total) * 100.,
                                                           (float(missed) / total) * 100.,
                                                           (float(wasted) / total) * 100.)

print r"""\end{tabularx}
}
\caption{\textbf{Accuracy of PocketParker predictions for various fraction of monitored drivers.}}
\label{table-accuracy}
\end{threeparttable}
\end{table}"""
