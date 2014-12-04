
def create_job(config):
  hadoop_dir = config["hadoop_dir"]
  path_to_streaming_jar = config["path_to_streaming_jar"]
  nosql_dir = config["nosql_dir"]
  input_path = config["input_path"]
  output_path = config["output_path"]
  mapper = config["mapper"]
  reducer = config["reducer"]

  copy_from_local = [hadoop_dir, "dfs", "-copyFromLocal", input_path, nosql_dir]
  map_reduce = [
      hadoop_dir, 
      "jar", path_to_streaming_jar, 
      "-file", mapper, "-mapper", mapper,
      "-file", reducer, "-reducer", reducer,
      "-input", input_path,
      "-output", output_path
  ]
  copy_to_local = [haddop_dir, "dfs", "-copyToLocal", output_path, "./"]

  return (copy_from_local, map_reduce, copy_to_local)


def execute(copy_from_local, map_reduce, copy_to_local):
  from subprocess import call
  call(copy_from_local)
  call(map_reduce)
  call(copy_to_local)


nosql_dir = "user/nosql/"
config = {
  "nosql_dir" : nosql_dir,
  "input_path" : "%sinput.txt" % nosql_dir,
  "output_path" : "%soutput.txt" % nosql_dir,
  "hadoop_dir" : "/usr/local/hadoop/bin/hadoop",
  "path_to_streaming_jar" : "/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.4.0.jar",
  "mapper" : "./mapper.py",
  "reducer" : "./reducer.py"
}

copy_from_local, map_reduce, copy_to_local = create_job(config)
execute(copy_from_local, map_reduce, copy_to_local)


