import csv
import os, sys
import re


def parse_csv(csv_path, column_separator, quote_char):
  with open(csv_path, 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=column_separator, quotechar=quote_char)
    for row in csv_reader:
      yield row

def yield_files(csv_dir, match_pattern=".*"):
  from os import listdir
  from os.path import isfile, join
  pattern = re.compile(match_pattern)
  result = []
  for f in listdir(csv_dir):
    if f.endswith(".csv") and isfile(join(csv_dir, f)):
      m = pattern.search(f)
      if m:
        result.append(m.group())
  return result

def fetch_years(header):
  years = []
  for column in header:
    if column.isdigit():
      years.append(int(column))
  return (years[0], years[-1])


class WorldBankParser():

  base = "%s/world_bank" % os.path.dirname(os.path.realpath(__file__))

  def __init__(self, csv_name):
    self.path_to_csv = "%s/%s" % (self.base, csv_name)
    self.sep = ","
    self.quote_char = '"'

  def parse(self):
    return list(parse_csv(self.path_to_csv, self.sep, self.quote_char))


class WorldBankIndicator():

  def __init__(self, csv_name):
    self.rows = WorldBankParser(csv_name).parse()
    self.title = self.rows[4][2]
    self.header_index = 2
    self.header = self.rows[self.header_index]
    self.start_year, self.latest_year = fetch_years(self.header)
    self.data = self.__data__(self.rows)

  def __data__(self, rows):
    result = {}
    for row in rows[(self.header_index + 1):]:
      country = row[0]
      result[country] = dict(zip(self.header, row))
    return result

  def __repr__(self):
    return "WorldBankIndicator<%s, %s-%s, size: %s>" % (self.title, self.start_year, self.latest_year, len(self.data))


class WorldBankWDI():

  def __init__(self, csv_name):
    self.rows = WorldBankParser(csv_name).parse()
    self.header_index = 0
    self.header = self.rows[self.header_index]
    self.start_year, self.latest_year = fetch_years(self.header)
    self.data = self.__data__(self.rows)

  def __data__(self, rows):
    result = {}
    for row in rows[(self.header_index + 1):]:
      country = row[0]
      indicator = row[2]
      sub_hash = dict(zip(self.header, row))
      if result.has_key(indicator):
        result[indicator][country] = sub_hash
      else:
        result[indicator] = { country : sub_hash }
    return result

  def __stats__(self):
    sub_sizes = [reduce(lambda a,y: a+1, x, 0) for (i, x) in self.data.iteritems()]
    sum_sizes = sum(sub_sizes) 
    return (
      len(self.data),
      sum_sizes / len(sub_sizes),
      sum_sizes
    )

  def __repr__(self):
    stats = self.__stats__()
    return "WorldBankWDI<%s-%s, indicators: %s, avg per indicator: %s, total: %s>" % (self.start_year, self.latest_year, stats[0], stats[1], stats[2])




def indicators():
  # http://data.worldbank.org/indicator/all
  csv_dir = "%s/world_bank" % os.path.dirname(os.path.realpath(__file__))
  for f in yield_files(csv_dir, ".*_[iI]ndicator_.*"):
    yield WorldBankIndicator(f)

def wdi_data():
  # download first 140mb! 
  # wget http://databank.worldbank.org/data/download/WDI_csv.zip
  # unzip WDI_Data.csv into project/world_bank folder 
  wdi_file = "WDI_Data.csv"
  return WorldBankWDI(wdi_file)


for indicator in indicators():
  print indicator
print wdi_data()



