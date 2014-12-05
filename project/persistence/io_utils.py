# coding: utf-8
import os
import json 
import ast
from utils import persistence_path


def save(apath, content):
  with open(apath, 'w+') as f:
    f.write(content)

def read(apath):
  t = ""
  with open(apath, 'r') as f:
    t = f.read()
  return t

# String -> Dictionary 
def load_json(fname):
  return ast.literal_eval(read(json_path(folders, fname)))

# Dictionary -> String -> Unit 
def save_json(fname, h):
  json_data = json.dumps(h, indent=2, sort_keys=True).encode('utf8')
  save("%s/%s" % (persistence_path(), fname)), json_data)
