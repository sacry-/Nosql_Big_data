import redis
import ast
from syntax import Words


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

  def exists(self, key_name):
    return self.rs.exists(key_name)

  def ping(self):
    print "ping: %s from: %s" % (self.rs.ping(), self)

  def flushdb(self):
    if raw_input("type 'flush' to kill data for db%s" % self.db) == "flush":
      self.rs.flushdb()
      print "successfully flushed db%s!" % self.db
    print "not flushed!"


class RContent(Rediss):

  def __init__(self, host="localhost", port=6379):
    super(RContent, self).__init__(host, port)
    self.db = 0
    self.rs = redis.Redis(host=self.host, port=self.port, db=self.db)

  def key_name(self, category, title):
    return "%s-content:%s" % (category, title)

  def __repr__(self):
    return "RContent %s with db%s" % (super(RContent, self).__repr__(), self.db)

  def values_by_pattern(self, pattern):
    for value in self.rs.mget(self.keys(pattern)):
      if value:
        yield value

  def key_value_by_pattern(self, pattern):
    pattern_keys = list(self.keys(pattern))
    all_values = self.rs.mget(pattern_keys)
    for (key, value) in zip(pattern_keys, all_values):
      if key and value:
        yield (key, value)

  def values_by_titles(self, category, titles):
    keys = map(lambda title: self.key_name(category, title), titles)
    for key in self.rs.mget(keys):
      if key:
        yield key

  def value_by_title(self, category, title):
    val = self.rs.get(self.key_name(category, title))
    if val:
      return val
    return {}

class RPos(Rediss):

  def __init__(self, host="localhost", port=6379):
    super(RPos, self).__init__(host, port)
    self.db = 1
    self.rs = redis.Redis(host=self.host, port=self.port, db=self.db)

  def key_name(self, category, title):
    return "%s-pos:%s" % (category, title)

  def put(self, category, title, content):
    super(RPos, self).put(category, title, Words(content).tags())

  def __repr__(self):
    return "RPos %s with db%s" % (super(RPos, self).__repr__(), self.db)


class RIdf(Rediss):

  def __init__(self, host="localhost", port=6379):
    super(RIdf, self).__init__(host, port)
    self.db = 2
    self.rs = redis.Redis(host=self.host, port=self.port, db=self.db)

  def key_name(self, category, title):
    return "%s-idf:%s" % (category, title)

  def put(self, category, title, content):
    super(RIdf, self).put(category, title, content)

  def __repr__(self):
    return "RIdf %s with db%s" % (super(RIdf, self).__repr__(), self.db)


class RFeature(Rediss):

  def __init__(self, host="localhost", port=6379):
    super(RFeature, self).__init__(host, port)
    self.db = 3
    self.rs = redis.Redis(host=self.host, port=self.port, db=self.db)

  def key_name(self, category, title):
    return "%s-feature:%s" % (category, title)

  def put(self, category, title, content):
    super(RFeature, self).put(category, title, content)

  def __repr__(self):
    return "RFeatures %s with db%s" % (super(RFeature, self).__repr__(), self.db)


# print map(str, RPos().values_by_pattern("biology-*"))
# print map(str, RContent().all_keys("biology-*"))

def test():
  titles = ["fluorenylmethyloxycarbonyl_chloride", "biology", 
  "biologist", "biological_ornament", "birth", "cell_population_data",
  "brian_dale", "dependence_receptor", "despeciation"]
  r_pos = RPos()
  print r_pos
  for elem in r_pos.values_by_titles("biology", titles):
    print len(elem)

# test()


