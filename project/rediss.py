import redis
import ast


LEVAL = ast.literal_eval

class Rediss(object):

  def __init__(self, host="localhost", port=6379):
    self.host = host
    self.port = port

  def __repr__(self):
    return "{ host='%s' port='%s' }" % (self.host, self.port)

  def keys(self, pattern="*"):
    for key in self.rs.keys(pattern): 
      yield key

  def real_title(self, redis_title):
    return redis_title.split(":", 1)[1]

  def values_by_pattern(self, pattern):
    for value in self.rs.mget(self.keys(pattern)):
      if value:
        yield LEVAL(value)

  def key_value_by_pattern(self, pattern):
    pattern_keys = list(self.keys(pattern))
    all_values = self.rs.mget(pattern_keys)
    for (key, value) in zip(pattern_keys, all_values):
      if key and value:
        yield (self.real_title(key), LEVAL(value))

  def values_by_titles(self, category, titles, ordered=False):
    keys = map(lambda title: self.key_name(category, title), titles)
    # ordered returns as many elemts as the input list was
    for key in self.rs.mget(keys):
      if key:
        yield LEVAL(key)
      else:
        if ordered:
          yield {}

  def value_by_title(self, category, title):
    val = self.rs.get(self.key_name(category, title))
    if val:
      return LEVAL(val)
    return {}

  def put(self, category, title, content):
    r = redis
    self.rs.set(self.key_name(category, title), content)

  def puts(self, category, mapping):
    self.rs.mset(
      dict(
        (self.key_name(category, title), str(value)) for title, value in mapping.iteritems()
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

  def exists(self, key_name):
    return self.rs.exists(key_name)

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




