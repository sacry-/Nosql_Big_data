import os, sys


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


nosql_dir = os.path.dirname(os.path.realpath(__file__))
nosql_files = "%s/files" % nosql_dir
config = {
  "input_path" : "%s/input.txt" % nosql_files,
  "output_path" : "%s/output.txt" % nosql_files,
  "mapper" : "%s/mapper.py" % nosql_files,
  "reducer" : "%s/reducer.py" % nosql_files,
  "hadoop_dir" : "/usr/local/hadoop/bin/hadoop",
  "path_to_streaming_jar" : "/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.4.0.jar"
}

print "nosql files dir: %s" % nosql_files
copy_from_local, map_reduce, copy_to_local = create_job(config)
execute(copy_from_local, map_reduce, copy_to_local)


