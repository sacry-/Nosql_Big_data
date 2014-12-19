import csv
import os, sys
import re


def project_path():
  return os.path.dirname(os.path.realpath(__file__))

def parse_csv(csv_path, column_separator, quote_char):
  with open(csv_path, 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=column_separator, quotechar=quote_char)
    for row in csv_reader:
      yield row

def yield_files(folder, extension, match_pattern=".*"):
  from os import listdir
  from os.path import isfile, join
  pattern = re.compile(match_pattern)
  result = []
  for f in listdir(folder):
    if f.endswith(extension) and isfile(join(folder, f)):
      m = pattern.search(f)
      if m:
        result.append(m.group())
  return result


class WorldBankParser():

  base = "%s/world_bank" % project_path()

  def __init__(self, csv_name):
    self.path_to_csv = "%s/%s" % (self.base, csv_name)
    self.sep = ","
    self.quote_char = '"'

  def parse(self):
    return list(parse_csv(self.path_to_csv, self.sep, self.quote_char))

