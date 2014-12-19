from pymongo import MongoClient
import ast
import re


# sudo mongod
# sudo mongo
# http://api.mongodb.org/python/current/tutorial.html
class Mongo(object):

  def __init__(self, host="localhost", port=27017):
    self.host = host
    self.port = port
    self.cl = MongoClient(host, port)


class MongoDB(Mongo):

  def __init__(self, db_name, host="localhost", port=27017):
    super(MongoDB, self).__init__(host, port)
    self.db = self.cl[db_name]

  def get(self, col_name):
    return self.db[col_name]

  def has_col(self, col_name):
    return col_name in self.db.collection_names()

post = {
  "author": "Mike",
  "text": "My first blog post!",
  "tags": ["mongodb", "python", "pymongo"]
}

# Builder
MongoDB("test1").get("posts1").insert(post)
MongoDB("test1").has_col("posts1")

c = MongoDB("test2").get("posts2")
c.insert(post)

# Object
mdb = MongoDB("test3")
c = mdb.get("posts3")
c.insert(post)
print mdb.has_col("posts3")
print c.find_one()




