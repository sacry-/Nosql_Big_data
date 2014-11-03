from pymongo import MongoClient
import ast
import readline

# aufgabe 7b
def get_city_and_state(collection, plz):
	res = collection.find_one({"_id":plz})
	return (res["city"], res["state"])

# aufgabe 7c
def plz_for_town(collection, town):
	res = collection.find_one({"city":town})
	return res["_id"]

#gui
def terminal():
	readline.parse_and_bind("tab: complete")
	
	#connect to mongodb
	m_client = MongoClient('localhost', 27017)
	#select db plz
	db = m_client.plz
	#select collection plz
	plz_collection = db.plz
	
	command = ""
	while command != "exit":
		if command.startswith("GETZIP"):
			try:
				command = command.split(" ")
				print "zip-code(s): %s" % plz_for_town(plz_collection, command[1])
			except:
				print "Value not found!"
		elif command.startswith("GETTOWN"):
			try:
				command = command.split(" ")
				res = get_city_and_state(plz_collection, command[1])
				print "(%s, %s)" % res
			except:
				print "Value not found!"
		else:
			print "commands exampels: GETZIP HAMBURG, GETTOWN 07419, exit"
		command = raw_input()

try:
  terminal() 
except:
  pass
print "bye bye"