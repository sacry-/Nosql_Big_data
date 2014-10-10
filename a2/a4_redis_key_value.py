import redis


def create_redis(host="localhost", kvs=("1337", 1337)):
  r_server = redis.Redis('localhost')
  r_server.set(kvs[0], kvs[1])                                  
  return r_server

def load_file():


def fill_redis_with_file_content():


r_server.set('counter', 1)
r_server.incr('counter')

r_server.decr('counter') #we decrease the key value by 1, has to be int
print 'the counter was decreased! '+ r_server.get('counter') #the key is back to normal


'''Now we are ready to jump into another redis data type, the list, notice 
that they are exactly mapped to python lists once you get them'''

r_server.rpush('list1', 'element1') #we use list1 as a list and push element1 as its element

r_server.rpush('list1', 'element2') #assign another element to our list
r_server.rpush('list2', 'element3') #the same

print 'our redis list len is: %s'% r_server.llen('list1') #with llen we get our redis list size right from redis

print 'at pos 1 of our list is: %s'% r_server.lindex('list1', 1) #with lindex we query redis to tell us which element is at pos 1 of our list

'''sets perform identically to the built in Python set type. Simply, sets are lists but, can only have unique values.'''

r_server.sadd("set1", "el1")
r_server.sadd("set1", "el2")
r_server.sadd("set1", "el2")

print 'the member of our set are: %s'% r_server.smembers("set1")

'''basically our redis client can do any command supported by redis, check out redis documentation for available commands for your server'''

