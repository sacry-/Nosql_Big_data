import re
from parsing import WorldBankParser
from parsing import project_path, yield_files


def fetch_years(header):
  years = []
  for column in header:
    if column.isdigit():
      years.append(int(column))
  return (years[0], years[-1])

def mongo_indicator_normalizer(s):
  s = s.strip().lower()
  s = re.sub('[\W\s]', '_', s)
  s = re.sub('\_+', '_', s)
  if s.endswith("_"):
    s = s[:-1]
  return re.sub('\$', '', s)

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
      country = self.__normalize__(row[0])
      normed_indicator = mongo_indicator_normalizer(row[2])
      indicator = self.__normalize__(row[2])
      sub_hash = dict(zip(self.header, row))
      if result.has_key(normed_indicator):
        result[normed_indicator][country] = sub_hash
      else:
        result[normed_indicator] = { country : sub_hash, "indicator" : indicator }
    return result

  def get_year_keys(self):
    return map(str, range(self.start_year, self.latest_year + 1))

  def __normalize__(self, s):
    s = s.strip().lower()
    return re.sub('\$', '', s)

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
  csv_dir = "%s/world_bank" % project_path()
  for f in yield_files(csv_dir, ".csv", ".*_[iI]ndicator_.*"):
    yield WorldBankIndicator(f)

def wdi_data():
  # download first 140mb! 
  # wget http://databank.worldbank.org/data/download/WDI_csv.zip
  # unzip WDI_Data.csv into project/world_bank folder 
  wdi_file = "WDI_Data.csv"
  return WorldBankWDI(wdi_file)

if __name__ == "__main__":
  for indicator in indicators():
    print indicator
  print wdi_data()



