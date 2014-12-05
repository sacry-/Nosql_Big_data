# coding: utf-8

import os, sys
p = "%s/../persistence" % os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, p)


import re
import enchant # pip install pyenchant
from nltk import word_tokenize
from nltk import data
from nltk import PorterStemmer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

from utils import persistence_path
from io_utils import read, load_json
from ast import literal_eval

# Pos Tagging
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger


STOPS = literal_eval(read(persistence_path() + "/love_the_data/stop_words.txt"))
SPECIAL = literal_eval(read(persistence_path() + "/love_the_data/special_characters.txt"))
LETTER_FREQ = dict(load_json("love_the_data","english-letter-frequencies")["letters"])
EN_US_DICT = enchant.Dict("en_US")
EN_GB_DICT = enchant.Dict("en_GB")
TAGGER = PerceptronTagger()
PORTER = PorterStemmer()
WN_LEMMATIZER = WordNetLemmatizer()
SENTENCE_DETECTOR = data.load('tokenizers/punkt/english.pickle')


'''
  CC Coordinating conjunction
  CD Cardinal number
  DT Determiner
  EX Existential there
  FW Foreign word
  IN Preposition or subordinating conjunction
  JJ Adjective
  JJR Adjective, comparative
  JJS Adjective, superlative
  LS List item marker
  MD Modal
  NN Noun, singular or mass
  NNS Noun, plural
  NNP Proper noun, singular
  NNPS Proper noun, plural
  PDT Predeterminer
  POS Possessive ending
  PRP Personal pronoun
  PRP$ Possessive pronoun
  RB Adverb
  RBR Adverb, comparative
  RBS Adverb, superlative
  RP Particle
  SYM Symbol
  TO to
  UH Interjection
  VB Verb, base form
  VBD Verb, past tense
  VBG Verb, gerund or present participle
  VBN Verb, past participle
  VBP Verb, non­3rd person singular present
  VBZ Verb, 3rd person singular present
  WDT Wh­determiner
  WP Wh­pronoun
  WP$ Possessive wh­pronoun
  WRB Wh­adverb
'''

# [(word, lemma, tag),..]

class Words():

  def __init__(self, text):
    self.tokens = wiki_tokenize(text)
    self.tokens_without_noise = remove_noise(self.tokens)
    self.pos_tags = pos_tag(" ".join(self.tokens_without_noise))
    self.pos_tags = stem_with_pos_tags(self.pos_tags)

  def tags(self):
    return self.pos_tags


def is_num(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def is_noisy(x):
  if x:
    x = x.strip().lower()
    return (
      # not be in stopwords
      x in STOPS or 
      # not be in specials
      re.match('(^\W+|\W+$)', x) or 
      x in SPECIAL or
      # should not be a num
      is_num(x) or 
      # should be larger than 1 i.e. not "a" etc.
      len(x) <= 1
    )
  else:
    return False

def word_is_valid(word):
  return (
    # word should not be none
    word and 
    # word should be valid in a english dictionary
    (EN_US_DICT.check(unicode(word)) and EN_GB_DICT.check(unicode(word))) or
    # average word length for biology assuming that the english word_list
    # does not contain specialized biology words
    (len(word) > 6 and
    # weird words containing large sequences of numbers are also included through
    # the lengths argument...
    not re.match(r'(\d{2,}.+|\w+\d{2,})', word))
  )

def remove_noise(tokens):
  return [remove_special(token) for token in tokens if not is_noisy(token)]

def remove_special(token):
  return re.sub("[\.\\\/\|,;\:\-\_\*\+\&\%\$\!\?\#]", "", token)

def wiki_tokenize(s):
  sentences = []
  for sentence in SENTENCE_DETECTOR.tokenize(s.strip()):
    if "See also" in sentence:
      return sentences
    if not any(delim in sentence for delim in ["http", "www", "://", "ISBN"]):
      sentences += word_tokenize(sentence)
  return sentences

def stemmatize(tokens): # work heavy!
  for token in tokens:
    if word_is_valid(token):
      yield PORTER.stem(WN_LEMMATIZER.lemmatize(token)).lower()

def lemmatize(tokens):
  for token in tokens:
    if word_is_valid(token):
      yield WN_LEMMATIZER.lemmatize(token).lower()

def stem(tokens):
  for token in tokens:
    if word_is_valid(token):
      yield PORTER.stem(token).lower()

# [(word, tag)..]
def stem_with_pos_tags(tagged_words):
  d = {}
  for (word, tag) in tagged_words:
    if word_is_valid(word):
      stemmed = PORTER.stem(word).lower()
      if d.has_key(stemmed):
        if d[stemmed].has_key(tag):
          d[stemmed][tag] = d[stemmed][tag] + 1
        else:
          d[stemmed][tag] = 1
      else:
        d[stemmed] = {tag : 1}
  return d

def pos_tag(text):
  blob = TextBlob(text, pos_tagger=TAGGER)
  return blob.tags
