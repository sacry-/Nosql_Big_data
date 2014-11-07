import os, sys
p = "%s/../a2" % os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, p)

import timeit
from a4_redis_key_value import create_redis, plz_for_town_r, get_city_and_state_r
from a7_mongodb import plz_for_town_m, get_city_and_state_m
from pymongo import MongoClient

N = 3000

print "comparing REDIS and MONGO with N=%s" % N
# PLZ REDIS
redis_plz_setup = '''
from a4_redis_key_value import create_redis, plz_for_town_r
r_server = create_redis(_host="localhost", _port=7777)
'''
redis_plz = timeit.Timer(stmt='plz_for_town_r(r_server, "HAMBURG")', setup=redis_plz_setup)
print "REDIS plz_for_town(HAMBURG) %s" % redis_plz.timeit(number=N)

# PLZ MONGO
mongo_plz_setup = '''
from a7_mongodb import plz_for_town_m
from pymongo import MongoClient
plz_collection = MongoClient('localhost', 27017).plz.plz
'''
mongo_plz = timeit.Timer(stmt='plz_for_town_m(plz_collection, "HAMBURG")', setup=mongo_plz_setup)
print "MONGO plz_for_town(HAMBURG) %s" % mongo_plz.timeit(number=N)

# CITY REDIS
redis_city_setup = '''
from a4_redis_key_value import create_redis, get_city_and_state_r
r_server = create_redis(_host="localhost", _port=7777)
'''
redis_city = timeit.Timer(stmt='get_city_and_state_r(r_server, "07419")', setup=redis_city_setup)
print "REDIS get_city_and_state(07419) %s" % redis_city.timeit(number=N)

# CITY MONGO
mongo_city_setup = '''
from a7_mongodb import get_city_and_state_m
from pymongo import MongoClient
plz_collection = MongoClient('localhost', 27017).plz.plz
'''
mongo_city = timeit.Timer(stmt='get_city_and_state_m(plz_collection, "07419")', setup=mongo_city_setup)
print "MONGO get_city_and_state(07419) %s" % mongo_city.timeit(number=N)


