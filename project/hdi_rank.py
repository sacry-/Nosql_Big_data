import re
from parsing import parse_csv
from parsing import project_path


def normalize(s):
  s = s.strip().lower()
  s = re.sub('[\W\s]', '_', s)
  s = re.sub('\_+', '_', s)
  if s.endswith("_"):
    s = s[:-1]
  return re.sub('\$', '', s)

def hdi_data():
  data = list(parse_csv("%s/world_bank/%s" % (project_path(), "hdi.csv"), ",", "'"))
  header = map(normalize, data[0])
  country_data = {}
  country_rank = {}
  for row in data[1:]:
    rank = row[0].strip()
    country = normalize(row[1])
    country_data[country] = dict(zip(header, row))
    if rank:
      country_rank[int(rank)] = country
      country_rank[country] = int(rank)
  return (country_data, country_rank)