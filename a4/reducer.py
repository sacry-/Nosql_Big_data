from itertools import groupby
from operator import itemgetter
import sys

def mapper_out(separator):
  for line in sys.stdin:
    yield line.rstrip().split(separator, 1)

def main(separator):
  for current_word, group in groupby(mapper_out(separator), itemgetter(0)):
    try:
      total_count = sum(map(lambda x: int(x[1]), group))
      print "%s%s%d" % (current_word, separator, total_count)
    except ValueError:
      pass

if __name__ == "__main__":
  main('\t')