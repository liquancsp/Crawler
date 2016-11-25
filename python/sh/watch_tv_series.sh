#!/bin/bash
cd ../
if [ ! -d "log" ]; then
   mkdir log
fi
if [ ! -d "data" ]; then
   mkdir data
fi
cd ./src/watch_tv_series
pwd
nohup python ./watch_tvseries_crawler.py -c ../../conf/watch_tv_series.conf &
