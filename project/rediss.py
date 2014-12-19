import redis
import ast


LEVAL = ast.literal_eval

def save_eval(obj):
  try:
    return LEVAL(obj)
  except:
    return obj

class Rediss(object):

  def __init__(self, host="localhost", port=6379):
    self.host = host
    self.port = port

  def __repr__(self):
    return "{ host='%s' port='%s' }" % (self.host, self.port)

  def keys(self, pattern="*"):
    for key in self.rs.keys(pattern): 
      yield key

  def values_by_pattern(self, pattern):
    for value in self.rs.mget(self.keys(pattern)):
      if value:
        yield save_eval(value)

  # Regex for keys -> [(key, value)..]
  def key_value_by_pattern(self, pattern):
    pattern_keys = list(self.keys(pattern))
    all_values = self.rs.mget(pattern_keys)
    for (key, value) in zip(pattern_keys, all_values):
      if key and value:
        yield (key, save_eval(value))

  # [key] -> [value]
  def values_by_keys(self, keys):
    for key in self.rs.mget(keys):
      if key:
        yield save_eval(key)

  def get_key(self, key):
    val = self.rs.get(key)
    if val:
      return save_eval(val)
    return {}

  def put(self, key, content):
    r = redis
    self.rs.set(key, content)

  def puts(self, mapping):
    self.rs.mset(
      dict(
        (key, str(value)) for key, value in mapping.iteritems()
      )
    )

  def pipeline(self, _transaction=False):
    return self.rs.pipeline(transaction=_transaction)

  def size(self):
    return self.rs.dbsize()

  def delete(self, keys):
    self.rs.delete(keys)
    return self.exists(keys[0])

  def take_by_pattern(self, pattern, n):
    for key, value in self.key_value_by_pattern(pattern):
      if n > 1:
        yield (key, value)
      else:
        break
      n -= 1

  def exists(self, key):
    return self.rs.exists(key)

  def ping(self):
    print "ping: %s from: %s" % (self.rs.ping(), self)

  def flushdb(self):
    if raw_input("type 'flush' to kill data for db%s" % self.db) == "flush":
      self.rs.flushdb()
      print "successfully flushed db%s!" % self.db
    print "not flushed!"


class RWorldBank(Rediss):

  def __init__(self, host="localhost", port=6379):
    super(RWorldBank, self).__init__(host, port)
    self.db = 0
    self.rs = redis.Redis(host=self.host, port=self.port, db=self.db)

  def __repr__(self):
    return "RWorldBank %s with db%s" % (super(RWorldBank, self).__repr__(), self.db)





