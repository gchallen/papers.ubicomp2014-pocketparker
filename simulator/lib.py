import copy, random, re, json, numpy, copy, StringIO

from scipy import misc
from lxml import etree

XML_SEPARATOR = "--------------------------"

def print_parameters(tree):
  print etree.tostring(tree.getroot(), pretty_print=True)
  print XML_SEPARATOR

def get_parameters(stream):
  xml = ""
  for line in stream:
    line = line.strip()
    if line == XML_SEPARATOR:
      return etree.parse(StringIO.StringIO(xml))
    xml += line

class Event(object):
  ARRIVAL = "A"
  DEPARTURE = "D"
  SEARCH = "S"

  def __init__(self, time, type):
    self.time, self.type, self.parked = time, type, False
    self.searched = []
    self.saw_search = False
    self.lot = None
    self.changed_lot = False

  @property
  def is_search(self):
    return self.type == self.SEARCH or self.type == self.ARRIVAL

  @property
  def is_arrival(self):
    return self.type == self.ARRIVAL
  
  @property
  def is_departure(self):
    return self.type == self.DEPARTURE

  def __repr__(self):
    s = "%.2f %s" % (self.time, self.type,)
    if self.type == 'S':
      s += " %s" % (self.lot.name,)
    if self.parked:
      s += " %s" % (self.lot.name,)
      if self.is_arrival and self.saw_search:
        s += " S"
        if len(self.searched) > 0:
          s += " [%s]" % ",".join([lot.name for lot in self.searched])
        else:
          s += " []"
    return s
 
  load_pattern = re.compile(r"(?P<time>[0-9\.]+)\s+(?P<type>(?:A|D))\s+(?P<lot>\S+)(?P<search>.*)")
  search_pattern = re.compile(r"S \[(?P<search>.*?)\]")
  @classmethod
  def loads(self, s, lots):
    s_match = Event.load_pattern.match(s)
    if s_match != None:
      e = Event(float(s_match.group('time')), s_match.group('type').strip())
      e.lot, e.parked = lots.get_lot(s_match.group('lot')), True
      if s_match.group('search').strip() != "":
        e.saw_search = True
        search_match = Event.search_pattern.match(s_match.group('search').strip())
        if search_match.group('search') != "":
          e.searched = [lots.get_lot(lot) for lot in search_match.group('search').split(",")]
      return e
    else:
      return None

def random_lot(lots):
  w = random.random() * sum([lot.weight for lot in lots])
  for i, lot in enumerate(lots):
    w -= lot.weight
    if w < 0:
      return lot

class Lots(object):
  def __init__(self, tree, verbose=False):
    self.lots = []
    for element in tree.xpath("//lot"):
      self.lots.append(Lot(element))

  def park(self, event):
    event.searched = []
    while True:
      if len(event.searched) == len(self.lots):
        break
      lot = random_lot([lot for lot in self.lots if lot not in event.searched])
      if not lot.park(event):
        event.searched.append(lot)
      else:
        event.lot, event.parked = lot, True
        break
    return event
  
  def leave(self, event):
    try:
      lot = random.choice([lot for lot in self.lots if not lot.empty])
      lot.leave(event)
      event.lot, event.parked = lot, True
    except IndexError:
      pass
    return event

  def get_lot(self, name):
    try:
      return [lot for lot in self.lots if lot.name == name][0]
    except IndexError:
      return None

  def print_capacity(self, time):
    return "\n".join(["%.2f C %s %d" % (time, lot.name, lot.count,) for lot in self.lots])

class Lot(object):
  def __init__(self, element, verbose=False):
    for key,type in {'name' : str, 'capacity': int,
                     'count': int, 'weight': float,
                     'poi': str, 'order': int}.items():
      setattr(self, key, type(element.get(key)))

  def park(self, event):
    if self.count + 1 > self.capacity:
      return False
    self.count += 1
    if self.count == self.capacity:
      event.changed_lot = True
    return True

  def leave(self, event):
    if self.count - 1 < 0:
      return False
    if self.count == self.capacity:
      event.changed_lot = True
    self.count -= 1
    return True
  
  @property
  def full(self):
    return self.count == self.capacity

  @property
  def empty(self):
    return self.count == 0

  def __repr__(self):
    if self.full:
      return "%s FULL" % (self.name,)
    else:
      return "%s AVAILABLE" % (self.name,)

  def __hash__(self):
    return self.name.__hash__()

HOURS_TO_SECONDS = 60 * 60.
MINUTES_TO_SECONDS = 60.
SECONDS_TO_SECONDS = 1.

encoded_pattern = re.compile(r"(?P<time>\d+)(?P<unit>\w)")
def convert_rate(encoded_rate):
  rate_match = encoded_pattern.match(encoded_rate)
  rate, unit = float(rate_match.group('time')), rate_match.group('unit')
  if unit == 'H':
    return rate / HOURS_TO_SECONDS
  elif unit == 'M':
    return rate / MINUTES_TO_SECONDS
  elif unit == 'S':
    return rate / SECONDS_TO_SECONDS
  else:
    raise Exception("Unknown rate code")

def convert_time(encoded_time):
  time_match = encoded_pattern.match(encoded_time)
  time, unit = float(time_match.group('time')), time_match.group('unit')
  if unit == 'H':
    return time * HOURS_TO_SECONDS
  elif unit == 'M':
    return time * MINUTES_TO_SECONDS
  elif unit == 'S':
    return rate * SECONDS_TO_SECONDS
  else:
    raise Exception("Unknown rate code")

class Rate(object):
  @classmethod
  def from_tree(cls, tree):
    return [Rate(element) for element in tree.xpath("//rate")]

  def __init__(self, element, verbose=False):
    for key,type in {'length': convert_time,
                     'arrival': convert_rate, 'departure': convert_rate}.items():
      setattr(self, key, type(element.get(key)))

  def events(self, start):
    self.time = start
    self.next_arrival, self.next_departure = None, None

    if self.arrival == 0. and self.departure == 0.:
      return
    while self.time < start + self.length:
      if self.next_arrival == None and self.arrival != 0.:
        self.next_arrival = self.time + random.expovariate(self.arrival)
      if self.next_departure == None and self.departure != 0.:
        self.next_departure = self.time + random.expovariate(self.departure)

      if self.next_arrival != None and (self.next_departure == None or self.next_arrival < self.next_departure):
        self.time = self.next_arrival
        if self.time > start + self.length:
          return
        yield Event(self.next_arrival, "A")
        self.next_arrival = None

      elif self.next_departure != None and (self.next_arrival == None or self.next_departure < self.next_arrival):
        self.time = self.next_departure
        if self.time > start + self.length:
          return
        yield Event(self.next_departure, "D")
        self.next_departure = None

      elif self.departure == self.next_arrival:
        self.time = self.next_departure
        if self.time > end:
          return
        yield Event(self.next_departure, "D")
        yield Event(self.next_arrival, "A")
        self.next_arrival = None
        self.next_departure = None

      else:
        raise Exception("Unknown problem with rate advance")

def seed_random(encoded_seed):
  if encoded_seed == None:
    return None
  else:
    random.seed(int(encoded_seed))
    return encoded_seed

class Simulation(object):
  def __init__(self, args):
    for key,type in {'monitored': float, 'search': float,
                     'arrival': float, 'departure': float,
                     'seed': seed_random}.items():
      setattr(self, key, type(getattr(args, key)))

  def saw_driver(self):
    return random.random() <= self.monitored
  
  def saw_arrival(self):
    return random.random() <= self.arrival
  
  def saw_departure(self):
    return random.random() <= self.departure

  def saw_search(self):
    return random.random() <= self.search

  def to_xml(self):
    element = etree.Element("simulation")
    for key in ['monitored', 'search', 'arrival', 'departure', 'seed']:
      element.set(key, str(getattr(self, key)))
    return element

class Estimation(object):
  def __init__(self, args, tree):
    for key,type in {'error': float, 'interval': convert_time,
                     'seed': seed_random, 'search': float,
                     'arrival_blank': int, 'departure_blank': int,
                     'search_blank': int, 'granularity': float}.items():
      setattr(self, key, type(getattr(args, key)))
    self.monitored = (1. + random.uniform(-1. * self.error, 1. * self.error)) \
        * float(tree.xpath("//simulation")[0].get("monitored"))
    self.lots = Lots(tree)

    self.time = {}
    self.search_window = {}
    self.departure_window = {}
    self.search_estimate = {}
    self.departure_estimate = {}
    self.count_estimate = {}
    self.lot_range = {}

    for lot in self.lots.lots:
      self.time[lot] = 0.
      self.search_window[lot] = []
      self.departure_window[lot] = []
      self.search_estimate[lot] = {}
      self.departure_estimate[lot] = {}
      self.count_estimate[lot] = {}
      self.lot_range[lot] = numpy.arange(-1 * lot.capacity, (2 * lot.capacity) + 1)
      count = 0
      for i in self.lot_range[lot]:
        if i < 0 or i > lot.capacity:
          self.count_estimate[lot][i] = 0.
        else:
          count += 1
          self.count_estimate[lot][i] = 1. / (lot.capacity + 1)
    self.test_counts()
  
  def to_xml(self):
    element = etree.Element("estimation")
    for key in ['error', 'interval', 'seed', 'search']:
      element.set(key, str(getattr(self, key)))
    return element

  def is_available(self, lot):
    return sum([count for i, count in self.count_estimate[lot].items() if i > 0])

  def test_counts(self, lots=None):
    if lots == None:
      lots = self.lots.lots
    for lot in lots:
      total_prob = round(sum(self.count_estimate[lot].values()), 4)
      if total_prob != 1.:
        raise Exception("Count estimates don't sum properly: %.2f" % (total_prob,))

  def fold_boundaries(self, lot):
    for i in self.lot_range[lot]:
      if i < 0:
        self.count_estimate[lot][0] += self.count_estimate[lot][i]
        self.count_estimate[lot][i] = 0
      elif i > lot.capacity:
        self.count_estimate[lot][lot.capacity] += self.count_estimate[lot][i]
        self.count_estimate[lot][i] = 0
    self.renormalize(lot)

  def renormalize(self, lot, test=True):
    if test:
      self.test_counts([lot])
    lot_sum = sum(self.count_estimate[lot].values())
    for i in self.lot_range[lot]:
      self.count_estimate[lot][i] /= lot_sum

  def searches(self, lot):
    self.search_window[lot] = \
        [e for e in self.search_window[lot] if e.time > self.time[lot] - self.interval]
    return self.search_window[lot]

  def num_searches(self, lot):
    return len(self.searches(lot))
  
  def departures(self, lot):
    self.departure_window[lot] = \
        [e for e in self.departure_window[lot] if e.time > self.time[lot] - self.interval]
    return self.departure_window[lot]

  def num_departures(self, lot):
    return len(self.departures(lot))

  def advance_time(self, lot, from_time):
    if from_time < self.time[lot] - self.interval:
      search_range = numpy.arange(0, lot.capacity * 2, 1)
      departure_range = numpy.arange(0, lot.capacity * 2, 1)

      search_rate_probabilities = {}
      for i in search_range:
        search_rate_probabilities[i] = misc.comb([i], [0])[0] * ((1 - self.monitored) ** i)
      search_sum = sum(search_rate_probabilities.values())
      for i in search_range:
        search_rate_probabilities[i] /= search_sum
      
      departure_rate_probabilities = {}
      for i in departure_range:
        departure_rate_probabilities[i] = misc.comb([i], [0])[0] * ((1 - self.monitored) ** i)
      departure_sum = sum(departure_rate_probabilities.values())
      for i in departure_range:
        departure_rate_probabilities[i] /= departure_sum
    
      while from_time < self.time[lot] - self.interval:
        count_estimate = copy.copy(self.count_estimate[lot])
        for i in self.lot_range[lot]:
          count_estimate[i] = 0.
          for j in self.lot_range[lot]:
            if j < i:
              continue
            if not search_rate_probabilities.has_key(j - i):
              continue
            count_estimate[i] += self.count_estimate[lot][j] * search_rate_probabilities[j - i]
        self.count_estimate[lot] = count_estimate
        
        count_estimate = copy.copy(self.count_estimate[lot])
        for i in self.lot_range[lot]:
          count_estimate[i] = 0.
          for j in self.lot_range[lot]:
            if j > i:
              continue
            if not departure_rate_probabilities.has_key(i - j):
              continue
            count_estimate[i] += self.count_estimate[lot][j] * departure_rate_probabilities[i - j]
        self.count_estimate[lot] = count_estimate

        self.fold_boundaries(lot)
        from_time += self.interval
        self.estimate_lot(lot, time=from_time)
    
    num_searches = int(round(self.num_searches(lot) * \
                             ((self.time[lot] - from_time) / self.interval),0))
    num_departures = int(round(self.num_departures(lot) * \
                               ((self.time[lot] - from_time) / self.interval),0))

    search_range = numpy.arange(num_searches, lot.capacity * 2, 1)
    departure_range = numpy.arange(num_departures, lot.capacity * 2, 1)

    search_rate_probabilities = {}
    for i in search_range:
      search_rate_probabilities[i] = misc.comb([i], [num_searches])[0] * \
          (self.monitored ** num_searches) * \
          ((1 - self.monitored) ** (i - num_searches))
    search_sum = sum(search_rate_probabilities.values())
    for i in search_range:
      search_rate_probabilities[i] /= search_sum
    
    departure_rate_probabilities = {}
    for i in departure_range:
      departure_rate_probabilities[i] = misc.comb([i], [num_departures])[0] * \
          (self.monitored ** num_departures) * \
          ((1 - self.monitored) ** (i - num_departures))
    departure_sum = sum(departure_rate_probabilities.values())
    for i in departure_range:
      departure_rate_probabilities[i] /= departure_sum
    
    count_estimate = copy.copy(self.count_estimate[lot])
    for i in self.lot_range[lot]:
      count_estimate[i] = 0.
      for j in self.lot_range[lot]:
        if j < i:
          continue
        if not search_rate_probabilities.has_key(j - i):
          continue
        count_estimate[i] += self.count_estimate[lot][j] * search_rate_probabilities[j - i]
    self.count_estimate[lot] = count_estimate
    
    count_estimate = copy.copy(self.count_estimate[lot])
    for i in self.lot_range[lot]:
      count_estimate[i] = 0.
      for j in self.lot_range[lot]:
        if j > i:
          continue
        if not departure_rate_probabilities.has_key(i - j):
          continue
        count_estimate[i] += self.count_estimate[lot][j] * departure_rate_probabilities[i - j]
    self.count_estimate[lot] = count_estimate

    self.fold_boundaries(lot)

  def estimate_lot(self, lot, time=None):
    if time == None:
      time = self.time[lot]
    print "P", lot.name, time, self.is_available(lot),
    step = int(lot.capacity * self.granularity)
    probs = []
    for limit in numpy.arange(0, lot.capacity, step):
      probs.append([limit, sum([prob for count, prob in self.count_estimate[lot].items() if count >= limit and count < limit + step])])
    probs[-1][1] += self.count_estimate[lot][lot.capacity]
    for count, prob in probs:
      print "%d:%.3f" % (count, prob),
    print

  def implicit_searches(self, event):
    better_lots = [lot for lot in self.lots.lots if lot != event.lot and lot.poi == event.lot.poi and lot.order < event.lot.order]
    if len(better_lots) == 0:
      return []
    implicit = []
    for lot in better_lots:
      if random.random() < self.search:
        search = Event(event.time, "S")
        search.lot = lot
        implicit.append(search)
    return implicit

  def event(self, event):
    last_time = self.time[event.lot]
    self.time[event.lot] = event.time
    
    if event.is_arrival:
      self.search_window[event.lot].append(event)
      for search in self.implicit_searches(event):
        self.search_window[search.lot].append(search)
        last_time = self.time[search.lot]
        self.time[search.lot] = event.time
        self.advance_time(search.lot, last_time)
        for i in numpy.arange(1, search.lot.capacity + 1, 1):
          self.count_estimate[search.lot][i] = self.count_estimate[search.lot][i + self.search_blank]
        self.count_estimate[search.lot][0] += sum([prob for count, prob in self.count_estimate[search.lot].items() if count > 0 and count < self.search_blank])
        self.renormalize(search.lot, test=False)

    elif event.is_departure:
      self.departure_window[event.lot].append(event)
    
    self.advance_time(event.lot, last_time)

    if event.is_arrival:
      for i in numpy.arange(0, self.arrival_blank + 1, 1):
        self.count_estimate[event.lot][i] = 0.
      self.renormalize(event.lot, test=False)
    elif event.is_departure:
      for i in numpy.arange(event.lot.capacity, (self.departure_blank - 1), -1):
        self.count_estimate[event.lot][i] = self.count_estimate[event.lot][i - (self.departure_blank)]
      for i in numpy.arange(0, self.departure_blank + 1, 1):
        self.count_estimate[event.lot][i] = 0.
      self.renormalize(event.lot, test=False)
    self.fold_boundaries(event.lot)
    
    print event
    self.estimate_lot(event.lot)
