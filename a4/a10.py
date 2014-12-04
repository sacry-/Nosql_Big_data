import os, sys
abs_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, "%s/../a2" % abs_file_path)

# /usr/local/Cellar/hbase/0.98.6.1/
# sudo hbase master start
# sudo hbase thrift start -threadpool
# _____________
# Unter dem hduser
# Hdoop starten:
# cd /usr/local/hadoop
# sbin/start-all.sh
#
# map_reduce starten:
# cd /home/hduser/Nosql_Big_data/a4/
# bash ./map_reduce.sh
# _______________________________
# Hbase: 
# ssh nosql@localhost
# cd /home/nosql/Downloads/hbase-0.98.7-hadoop2/
# ./bin/start-hbase.sh (Hbase Start)
#
# Thrift:
# ./bin/hbase thrift start
#


import happybase
from a4_redis_key_value import load_file

def data_exists(table):
  return len([key for key, data in table.rows(['01001', '47270', '99950'])]) == 3

def populate_hbase(table):
  print "setting up table"
  list_of_hashes = load_file("%s/files/plz.data" % abs_file_path)
  for h in list_of_hashes:
    zip_code = h["_id"]
    h.pop("_id", None)
    result = {}
    for key, value in h.iteritems():
      result["%s:%s" % ("zip", key)] = str(value)
    val = ""
    if result["zip:city"] in ["HAMBURG", "BREMEN"]:
      val = "ja"
    result["%s:%s" % ("fussball", "city")] = val
    table.put(zip_code, result)

def setup_and_table():
  connection = happybase.Connection(host='localhost', port=9090)
  print "opening connection"
  connection.open()
  print "connection opened"

  print connection.tables()
  db_name = "plz_data"
  try:
    connection.create_table(db_name, {'zip': dict(), "fussball" : dict()})
    print "successfully created table!"
  except:
    print "table already exists"

  table = connection.table(db_name)
  print "tables: %s" % connection.tables()

  return table

# aufgabe 10c
def get_city_and_state_h(table, plz):
  d = table.row(plz)
  return (d["zip:city"], d["zip:state"])

# aufgabe 10d
def plz_for_town_h(table, town):
  return [key for key, data in table.scan(columns=['zip:city']) if data["zip:city"] == town]

# aufgabe 10b test
def football_for_town(table, town):
  for plz in plz_for_town_h(table, town):
    d = table.row(plz)
    yield (d["zip:city"], d["zip:state"], d["fussball:city"])


table = setup_and_table()

if not data_exists(table):
  populate_hbase(table)
else:
  print "data already in table!"


print get_city_and_state_h(table, '47270')
print plz_for_town_h(table, 'HAMBURG')

print list(football_for_town(table, 'HAMBURG'))
print list(football_for_town(table, 'BELCHERTOWN'))






