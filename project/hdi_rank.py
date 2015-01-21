import re
from parsing import parse_csv
from parsing import project_path


class HDIRank():

  def __init__(self):
    self.data = list(parse_csv("%s/world_bank/%s" % (project_path(), "hdi.csv"), ",", "'"))
    self.header = map(self.__normalize__, self.data[0])
    self.country_data = {}
    self.country_rank = {}

  def __normalize__(self, s):
    s = s.strip().lower()
    s = re.sub('[\W\s]', '_', s)
    s = re.sub('\_+', '_', s)
    if s.endswith("_"):
      s = s[:-1]
    return re.sub('\$', '', s)

  def create_rank(self):
    self.worst_rank = 0
    for row in self.data[1:]:
      rank = row[0].strip()
      country = self.__normalize__(row[1])
      self.country_data[country] = dict(zip(self.header, row))
      if rank:
        rank = int(rank)
        if rank > self.worst_rank:
          self.worst_rank = rank
        self.country_rank[rank] = country
        self.country_rank[country] = rank

  def top(self, n):
    result = []
    for rank in range(1, n + 1):
      result.append( self.country_rank[rank] )
    return result

  def lowest(self, n):
    result = []
    for rank in range(0, n):
      r = self.worst_rank - rank
      result.append( self.country_rank[r] )
    return result

  def goods_bads(self, tops):
    self.create_rank()
    return (self.top(tops), self.lowest(tops))


