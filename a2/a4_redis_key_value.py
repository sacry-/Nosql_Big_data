import redis
import ast

#decode JSON
def string_to_hash(json_string):
	return ast.literal_eval(json_string)

# aufgabe 4a
#open file and decode json lines
def load_file(apath):
	f = open(apath, 'r')
  	result = []
  	for line in f:
		result.append(string_to_hash(line))
  	f.close()
  	return result

#add Hash h to Redis
def populate_redis_with_hash(r_server, h):
  for elem in h:
    r_server.set(elem["_id"], elem)
    r_server.rpush(elem["city"], elem["_id"])
  print "Populated!"

#connect to redis and load data if not in db
def create_redis():
	r_server = redis.Redis('localhost')
	if not r_server.exists("13063"):
		print "No Data exists, importing plz.data..."
		h = load_file("./plz.data")
		populate_redis_with_hash(r_server, h)
	return r_server

def get_key(r_server, plz):
  return string_to_hash(r_server.get(plz))

# aufgabe 4b
def get_city_and_state(r_server, plz=""):
	if not plz:
		plz = raw_input("Bitte eine PLZ angeben: ")
  res = get_key(r_server, plz)
  return (res["city"], res["state"])

# aufgabe 4c
def plz_for_town(r_server, town):
  return r_server.lrange(town, 0, r_server.llen(town))

# aufgabe 4c
def plz_for_town_slow(r_server, town):
  for key in r_server.keys("[0-9][0-9]*"):
    if get_key(r_server, key)["city"] == town:
      yield key

r_server = create_redis()
print get_city_and_state(r_server, "13063")

print plz_for_town(r_server, "HAMBURG")
print plz_for_town(r_server, "TUMTUM")

# aufgabe 4c
def plz_for_town(r_server, town=""):
	if(town==""):
		town = raw_input("Bitte eine Stadt angeben: ")
	return r_server.lrange(town, 0, r_server.llen(town))


#gui
def gui_start():
	r_server = create_redis()
	command = ""
	while command != "exit":
		if command == "GETPLZ":
			print "Postleitzahl: %s" %plz_for_town(r_server)
		elif command == "GETTOWN":
			res = get_city_and_state(r_server)
			print "Stadt: {0} | Staat: {1}".format(res[0],res[1])
		else:
			print "Kommandos: GETPLZ, GETTOWN, exit"
		command = raw_input()
	print "Beendet."

gui_start() 
	
#print get_city_and_state(r_server, "13063")
#print plz_for_town(r_server, "HAMBURG")
#print plz_for_town(r_server, "TUMTUM")
