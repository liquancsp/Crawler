#!/bin/bash
cd ../
if [ ! -d "log" ]; then
   mkdir log
fi
if [ ! -d "data" ]; then
   mkdir data
fi
cd ./src/tencent
pwd
nohup python ./tencent_tv_crawler.py -c ../../conf/tencent_tv.conf &
