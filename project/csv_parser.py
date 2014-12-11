import csv
import os, sys


def parse_csv(csv_path, column_separator, quote_char):
  with open(csv_path, 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=column_separator, quotechar=quote_char)
    for row in csv_reader:
      yield row

def yield_files(csv_dir):
  from os import listdir
  from os.path import isfile, join
  return [f for f in listdir(csv_dir) if isfile(join(csv_dir, f))]


class WorldBankParser():

  base = "%s/world_bank" % os.path.dirname(os.path.realpath(__file__))

  def __init__(self, csv_name):
    self.path_to_csv = "%s/%s" % (self.base, csv_name)
    self.sep = ","
    self.quote_char = '"'

  def parse(self):
    return list(parse_csv(self.path_to_csv, self.sep, self.quote_char))


class WorldBankData():

  def __init__(self, csv_name):
    self.rows = WorldBankParser(csv_name).parse()
    self.title = self.rows[4][2]
    self.header_index = 2
    self.header = self.rows[self.header_index]
    self.start_year, self.latest_year = self.__fetch_years__(self.header)
    self.data = self.__data__(self.rows)

  def __fetch_years__(self, header):
    years = []
    for column in header:
      if column.isdigit():
        years.append(int(column))
    return (years[0], years[-1])

  def __data__(self, rows):
    result = {}
    for row in rows[(self.header_index + 1):]:
      country = row[0]
      result[country] = dict(zip(self.header, row))
    return result

  def __repr__(self):
    return "WorldBankData<%s, %s-%s, size: %s>" % (self.title, self.start_year, self.latest_year, len(self.data))


def test():
  for f in yield_files("%s/world_bank" % os.path.dirname(os.path.realpath(__file__))):
    print WorldBankData(f)


test()
