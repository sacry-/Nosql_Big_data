

def create_job(config):
  hadoop_dir = config["hadoop_dir"]
  path_to_streaming_jar = config["path_to_streaming_jar"]
  input_path = config["input_path"]
  output_path = config["output_path"]
  mapper = config["mapper"]
  reducer = config["reducer"]

  copy_from_local = [hadoop_dir, "dfs", "-copyFromLocal", input_path]
  map_reduce = [
      hadoop_dir, 
      "jar", path_to_streaming_jar, 
      "-file", mapper, "-mapper", mapper,
      "-file", reducer, "-reducer", reducer,
      "-input", input_path,
      "-output", output_path
  ]
  copy_to_local = [hadoop_dir, "dfs", "-copyToLocal", output_path]

  return (copy_from_local, map_reduce, copy_to_local)


def execute(copy_from_local, map_reduce, copy_to_local):
  from subprocess import call
  call(copy_from_local)
  call(map_reduce)
  call(copy_to_local)


def create_config(nosql_dir=None, hadoop_home=None, stream_jar=None):
  if not nosql_dir: 
    from os import path
    nosql_dir = path.dirname(path.realpath(__file__))
  if not hadoop_home: 
    hadoop_home = "/usr/local/hadoop/bin/hadoop"
  if not stream_jar: 
    stream_jar = "/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.4.0.jar"

  print "nosql dir: %s" % nosql_dir
  print "hadoop home: %s" % hadoop_home
  print "streaming jar: %s" % stream_jar

  nosql_files = "%s/files" % nosql_dir
  config = {
    "input_path" : "%s/input.txt" % nosql_files,
    "output_path" : "%s/output.txt" % nosql_files,
    "mapper" : "%s/mapper.py" % nosql_files,
    "reducer" : "%s/reducer.py" % nosql_files,
    "hadoop_dir" : hadoop_home,
    "path_to_streaming_jar" : stream_jar
  }
  return config


def parse_args():
  from argparse import ArgumentParser
  parser = ArgumentParser(description="start map reduce job")
  parser.add_argument('-nosql_dir', action='store', metavar="NOSQL_PROJECT", help="nosql project dir")
  parser.add_argument('-hadoop_home', action='store', metavar="HADOOP_HOME", help="hadoop excute dir")
  parser.add_argument('-stream_jar', action='store', metavar="HADOOP_STREAM", help="hadoop streaming jar")
  args = parser.parse_args()
  return (args.nosql_dir, args.hadoop_home, args.stream_jar)


# uses defaults: python map_reduce_job.py
# uses provided paths: python map_reduce_job.py -hadoop_home=abc/de -stream_jar=abc/de
def run_job():
  nosql_dir, hadoop_home, stream_jar = parse_args()
  config = create_config(nosql_dir, hadoop_home, stream_jar)
  copy_from_local, map_reduce, copy_to_local = create_job(config)
  execute(copy_from_local, map_reduce, copy_to_local)


run_job()





