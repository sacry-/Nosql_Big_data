#!/bin/bash
rm -rf output1

hadoop jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar -input files/input.txt -output output1 -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py 

hadoop fs -cat output1/part-00000
