import re
import mongo
import enchant
from nltk import WordNetLemmatizer


STOPS = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
WN_LEMMATIZER = WordNetLemmatizer()
EN_US_DICT = enchant.Dict("en_US")
EN_GB_DICT = enchant.Dict("en_GB")


def all_countries(mdb):
  coll = mdb.get("urban_population")
  result = set([])
  for entry in coll.find({"country" : { "$regex" : re.compile(".+", re.IGNORECASE)}}):
    result.add( entry["country"] )
  return list(result)

def tokenize(indicators):
  return list(set(sum(map(lambda x: x.split("_"), indicators), [])))

def filter_stops(words, countries):
  p = re.compile("[a-z]+")
  return filter(lambda w: not w in STOPS and p.match(w) and not w in countries, words)

def word_is_valid(word):
  return (EN_US_DICT.check(unicode(word)) and EN_GB_DICT.check(unicode(word)) and len(word) > 2)

def lemmatize(tokens): # work heavy!
  result = set([])
  for token in tokens:
    if word_is_valid(token):
      result.add( WN_LEMMATIZER.lemmatize(token).lower() )
  return list(result)


mdb = mongo.MongoDB("wdi_data")
c = mdb.collections()
tokens = tokenize(c)
countries = all_countries(mdb)
clean_tokens = filter_stops(tokens, countries)
lems = sorted(list(lemmatize(clean_tokens)))
print lems
print len(lems)
