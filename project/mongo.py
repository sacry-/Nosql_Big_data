from pymongo import MongoClient
import ast
import re

from world_bank import wdi_data

# sudo mongod
# sudo mongo
# http://api.mongodb.org/python/current/tutorial.html
class Mongo(object):

  def __init__(self, host="localhost", port=27017):
    self.host = host
    self.port = port
    self.cl = MongoClient(host, port)

class MongoDB(Mongo):

  def __init__(self, db_name, host="localhost", port=27017):
    super(MongoDB, self).__init__(host, port)
    self.db = self.cl[db_name]

  def get(self, col_name):
    return self.db[col_name]

  def has_col(self, col_name):
    return col_name in self.collections()

  def collections(self):
    return self.db.collection_names()

  def has_data(self, n):
    already_migrated = len(self.collections()) > n
    if already_migrated:
      print "No migration necessary!"
    else:
      print "Migration necessary!"
    return already_migrated


def time_series_query(coll):
  regx = re.compile("[0-9E\+\.]+", re.IGNORECASE)
  years = map(str, range(1980, 2014 + 1))
  query = {"$or" : [{"years.%s" % year : { "$regex": regx }} for year in years]}
  for entry in coll.find(query):
    yield entry

def test_mongo(mdb):
  if not mdb.has_data(1300):
    migrate_world_bank_data(mdb)
  name = "women_who_believe_a_husband_is_justified_in_beating_his_wife_when_she_goes_out_without_telling_him"
  coll = mdb.get(name)
  result = ", ".join( sorted([entry["country"] for entry in time_series_query(coll)]) )
  print name
  print result

def migrate_world_bank_data(mdb):
  wdi = wdi_data()
  print wdi
  for nindicator, countries in wdi.data.iteritems():
    if len(countries["indicator"]) >= 110:
      continue
    c = mdb.get(nindicator)
    c.insert({"indicator" : countries["indicator"]})
    for country, time_data in countries.iteritems():
      years = []
      for year in wdi.get_year_keys():
        try:
          years.append({ year : time_data[year] })
        except:
          pass
      c.insert({
        "country" : country,
        "years" : years
      })
    print c.find_one()


if __name__ == "__main__":
  mdb = MongoDB("wdi_data")
  test_mongo(mdb)


