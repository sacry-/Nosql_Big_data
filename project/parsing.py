import csv
import os, sys
import re
import xml.etree.ElementTree as ET

def project_path():
  return os.path.dirname(os.path.realpath(__file__))

def parse_csv(csv_path, column_separator, quote_char):
  with open(csv_path, 'rb') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=column_separator, quotechar=quote_char)
    for row in csv_reader:
      yield row

def parse_xml(xml_path, indicator) :
  tree = ET.parse(xml_path)
  root = tree.getroot()

  data = dict()

  for child in root.iter("record"):
    record = dict()
    for field in child.findall("field"):
      field_name = field.get("name")
      field_value = field.text

      if field_value:
        if field_name == "Country or Area":
          country = field_value.replace(".","")
          
          record["Country"] = country
        elif field_name == "Year(s)":
          record["Year"] = field_value
        else:  
          record[field_name] = field_value

    if record:
      data.setdefault(country+"."+indicator+"."+record["Year"],[])
      data[country+"."+indicator+"."+record["Year"]].append(record)

  return data

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

class UnDataParser():
  base = "%s/undata" % project_path()

  def __init__(self, xml_name, indicator):
    self.indicator = indicator
    self.path_to_xml = "%s/%s" % (self.base, xml_name)

  def parse(self):
    a = parse_xml(self.path_to_xml, self.indicator)
    return a