import redis
import ast

def string_to_hash(s):
  return ast.literal_eval(s)

# aufgabe 4a
def load_file(apath):
  f = open(apath, 'r')
  result = []
  for line in f:
    result.append(string_to_hash(line))
  f.close()
  return result

def populate_redis_with_hash(r_server, h):
  result = []
  for elem in h:
    r_server.set(elem["_id"], elem)
    r_server.rpush(elem["city"], elem["_id"])
  print "Populated!"

def create_redis():
  r_server = redis.Redis('localhost')
  if not r_server.exists("13063"):
    h = load_file("/Users/sacry/dev/uni/s5/nosql/Nosql_Big_data/a2/plz.data")
    populate_redis_with_hash(r_server, h)
  return r_server


# aufgabe 4b
def get_city_and_state(r_server, plz):
  res = string_to_hash(r_server.get(plz))
  return (res["city"], res["state"])

# aufgabe 4c
def plz_for_town(r_server, town):
  return r_server.lrange(town, 0, r_server.llen(town))

r_server = create_redis()
print get_city_and_state(r_server, "13063")

print plz_for_town(r_server, "HAMBURG")
print plz_for_town(r_server, "TUMTUM")






