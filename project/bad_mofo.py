import mongo
import time
import re
from hdi_rank import HDIRank


def values_for_entry(entry):
  result = []
  for entry in entry["years"]:
    for year, num in entry.items():
      try:
        result.append( float(num) )
      except:
        pass
  return result

def average_list(l):
  try:
    return sum(l) / len(l)
  except:
    return None

def average_entry(entry):
  return average_list(values_for_entry(entry))

def average_by(data, biased_countries):
  elems = []
  for entry in data:
    if entry["country"].lower() in biased_countries:
      elems += values_for_entry(entry)
  return average_list(elems)

def heuristic(entry, good_avg, bad_avg):
  c = entry["country"]

  country_average = average_entry(entry)
  r1 = 0.8 * abs(country_average - good_avg)
  r2 = abs(country_average - bad_avg)

  gc, bc = 0, 0 
  if good_avg > bad_avg:
    if r1 < r2:
      gc = 1
    else: # r1 < r2
      bc = 1
  elif good_avg < bad_avg:
    if r1 > r2:
      gc = 1
    else: # r1 > r2
      bc = 1

  return (c, gc, bc)

def count(h, k, amount):
  if not h.has_key(k):
    h[k] = 0
  h[k] += amount
  return h

def interpret(mdb, indicators, biased_good, biased_bad):

  # Results
  good_countries, bad_countries = {}, {}

  for idx, indicator in enumerate(indicators):

    # Retrieve time series data from MongoDB
    collection = mdb.get(indicator)
    data = list(mongo.time_series_query(collection))

    # Calculate averages for good and bad values
    good_avg = average_by(data, biased_good)
    bad_avg = average_by(data, biased_bad)
    if not good_avg or not bad_avg:
      continue

    print idx + 1, "%s%s" % ((indicator, "") if len(indicator) < 50 else (indicator[:47], "..."))

    for entry in data:
      # Calculate by heuristic if some country is nearer
      # to the good or bad average
      country, gc, bc = heuristic(entry, good_avg, bad_avg)
      # Assign the count to resulting countries
      good_countries = count(good_countries, country, gc) 
      bad_countries = count(bad_countries, country, bc)

  return (
    # Sort by highest counted countries
    sorted(good_countries.items(), key=lambda x: -x[1]), 
    sorted(bad_countries.items(), key=lambda x: -x[1])
  )


def print_seq(seq, n, msg):
  print msg
  for idx, (c, v) in enumerate(seq[:n]):
    print "%s. %s : %s" % (idx + 1, c, v)



mdb = mongo.MongoDB("wdi_data")
mongo.test_mongo(mdb)

n = 15
indicators = mdb.collections()

t1 = time.time()

hdi_good, hdi_bad = HDIRank().goods_bads(n)

gsize, bsize = len(hdi_good) / 2, len(hdi_bad) / 2
biased_good = hdi_good[:gsize] + hdi_bad[:bsize]
biased_bad = hdi_good[gsize:] + hdi_bad[bsize:]

good, bad = interpret(mdb, indicators, biased_good, biased_bad)

print "%s\n%s" % (biased_bad, biased_good)
print_seq(good, n, "top %s goods:" % n)
print_seq(bad, n, "top %s bads:" % n)

t2 = time.time()
print "time elapsed: %s" % (t2 - t1)




