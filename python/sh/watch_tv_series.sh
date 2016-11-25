#!/bin/bash
cd ../src/watch_tv_series & pwd & nohup python ./watch_tvseries_crawler.py -c ../../conf/watch_tv_series.conf &
