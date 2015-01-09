#Downloading UNData:

#Total population, both sexes combined (thousands):
#http://data.un.org/Data.aspx?d=PopDiv&f=variableID%3a12&c=2,4,6,7&s=_crEngNameOrderBy:asc,_timeEngNameOrderBy:desc,_varEngNameOrderBy:asc&v=1
#indicator suffix: population

#Gender Parity Index in primary level enrolment
#http://data.un.org/Data.aspx?d=MDG&f=seriesRowID:611&c=2,3,4&s=countryEnglishName:asc,year:desc&v=1
#indicator suffix: gpi_primary

#Gender Parity Index in secondary level enrolment
#http://data.un.org/Data.aspx?d=MDG&f=seriesRowID%3a613&c=2,3,4&s=countryEnglishName:asc,year:desc&v=1
#indicator suffix: gpi_secondary

#Gender Parity Index in tertiary level enrolment
#http://data.un.org/Data.aspx?d=MDG&f=seriesRowID:614&c=2,3,4&s=countryEnglishName:asc,year:desc&v=1
#indicator suffix: gpi_teritary

#Percentage of individuals using the Internet
#http://data.un.org/Data.aspx?d=ITU&f=ind1Code:I99H&c=2,3,4&s=countryName:asc,year:desc&v=1
#indicator suffix: internetusers

#GDP (current US$)
#http://data.un.org/Data.aspx?d=WDI&f=Indicator_Code:NY.GDP.MKTP.CD&c=2,4,5&s=Country_Name:asc,Year:desc&v=1
#indcator suffix: gpi_usd

#Beer
#http://data.un.org/Data.aspx?d=ICS&f=cmID:24310-0&c=2,3,5,6&s=_crEngNameOrderBy:asc,yr:desc,_utEngNameOrderBy:asc&v=1
#indicator suffix: beer


#Download as xml
#unzip to project/undata
#Rename to undata_*suffix*.xml



from parsing import UnDataParser
from parsing import project_path, yield_files
from rediss import RUnData

def key_to_dict(key):
  res = dict()
  keys = key.split(".")
  if len(keys)==3:
    res["Country"] = keys[0]
    res["Indicator"] = keys[1]
    res["Year"] = int(keys[2])
  return res

def dict_to_key(dict):
  return dict["Country"]+"."+dict["Indicator"]+"."+str(dict["Year"])

def fetch_years(data):
  years = []
  min_year = 9999
  max_year = 0
  for key,value in data.items():
      item = key_to_dict(key)
      if len(item)>0:
        if item["Year"]<min_year:
          min_year = item["Year"]
        if item["Year"]>max_year:
          max_year = item["Year"]

  return (min_year, max_year)

class UnDataIndicator():

  def __init__(self, xml_name, title):
    self.title = title
    self.rows = UnDataParser(xml_name, self.title).parse()
    self.data = self.__data__(self.rows)
    self.start_year, self.latest_year = fetch_years(self.data)
    #rint "Value : %s" %  self.data.keys()

  def __data__(self, rows):
    return rows

  def __repr__(self):
    return "UnDataIndicator<%s, %s-%s size: %s>" % (self.title, self.start_year, self.latest_year, len(self.data))

def indicators():
  xml_dir = "%s/undata" % project_path()
  for f in yield_files(xml_dir, ".xml", "undata_.*"):
    title = f.replace("undata_","")
    title = title.replace(".xml","")

    yield UnDataIndicator(f,title)

def undata_to_redis():
  rundata = RUnData()
  for indicator in indicators():
    rundata.puts(indicator.data)

for indicator in indicators():
  print indicator
  if indicator.title=="beer":
    print indicator.data[dict_to_key({"Indicator":"beer","Country":"Germany","Year":2010})]

  undata_to_redis()