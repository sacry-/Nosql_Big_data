#!/usr/bin/env python
import sys

def lines():
  for line in sys.stdin:
    yield line.split()

def main():
  for words in lines():
    for word in words:
      print '%s%s%d' % (word, '\t', 1)

if __name__ == "__main__":
  main()