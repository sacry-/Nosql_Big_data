from parsing import UnDataParser
from parsing import project_path, yield_files
from rediss import RUnData

def key_to_dict(key):
  res = dict()
  keys = key.split(".")
  if len(keys)==3:
    res["country"] = keys[0]
    res["indicator"] = keys[1]
    res["year"] = int(keys[2])
  return res

def dict_to_key(key_dict):
  return key_dict["country"]+"."+key_dict["indicator"]+"."+str(key_dict["year"])

def fetch_years(data):
  years = []
  min_year = 9999
  max_year = 0
  for key,value in data.items():

      item = key_to_dict(key)
      if len(item)>0:
        if item["year"]<min_year:
          min_year = item["year"]
        if item["year"]>max_year:
          max_year = item["year"]

  return (min_year, max_year)

class UnDataindicator():

  def __init__(self, xml_name, title):
    self.title = title
    self.rows = UnDataParser(xml_name, self.title).parse()
    self.data = self.__data__(self.rows)
    self.start_year, self.latest_year = fetch_years(self.data)
    #rint "Value : %s" %  self.data.keys()

  def __data__(self, rows):
    return rows

  def __repr__(self):
    return "UnDataindicator<%s, %s-%s size: %s>" % (self.title, self.start_year, self.latest_year, len(self.data))

def indicators():
  xml_dir = "%s/undata" % project_path()
  for f in yield_files(xml_dir, ".xml", "undata_.*"):
    title = f.replace("undata_","")
    title = title.replace(".xml","")

    yield UnDataindicator(f,title)

def undata_to_redis():
  rundata = RUnData()
  for indicator in indicators():
    rundata.puts(indicator.data)

undata_to_redis()