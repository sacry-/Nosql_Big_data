import os, sys
abs_file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, "%s/../a2" % abs_file_path)


import happybase
from a4_redis_key_value import load_file

def data_exists(table):
  return len([key for key, data in table.rows(['01001', '47270', '99950'])]) == 3

def populate_hbase(table):
  list_of_hashes = load_file("%s/plz.data" % abs_file_path)
  for h in list_of_hashes:
    zip_code = h["_id"]
    h.pop("_id", None)
    result = {}
    for key, value in h.iteritems():
      result["%s:%s" % ("family", key)] = str(value)
    table.put(zip_code, result)

def setup_and_table():
  connection = happybase.Connection('localhost')
  connection.open()

  db_name = "zip2"
  try:
    connection.create_table(db_name, {'family': dict(), "Fussball" : dict()})
  except:
    print "already exists"

  table = connection.table(db_name)
  print "tables: %s" % connection.tables()

  return table

table = setup_and_table()

if not data_exists(table):
  populate_hbase(table)

# aufgabe 10c
def get_city_and_state_h(table, plz):
  d = table.row(plz)
  return (d["family:city"], d["family:state"])

# aufgabe 10d
def plz_for_town_h(table, town):
  return [key for key, data in table.scan(columns=['family:city']) if data["family:city"] == town]

# print get_city_and_state_h(table, '47270')
# print plz_for_town_h(table, 'HAMBURG')


