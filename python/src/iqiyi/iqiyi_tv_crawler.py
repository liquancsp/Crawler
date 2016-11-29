import sys
import codecs
import re
import csv
import urllib2
sys.path.append("..")
import tools.network_tool as nt
import tools.json_tools as jt
from tools.logger_tool import *
from optparse import OptionParser

def fetch_tv_total_page(conf_json) :
	page_num = 1
	while True:
		content = nt.fetchUrlContent(conf_json["url"].format(page_num))
		if content != None:
			content = content.replace('\n', '').replace('\t', '')
		pattern = re.compile(conf_json["tv_total_page_pattern"])
		match_data = re.findall(pattern, content)
		logger.info('page_num : {},  match_data : {}'.format(page_num, int(match_data[-1])))
		if page_num >= int(match_data[-1]) :
			logger.info('find max page num!')
			return page_num
		else :
			page_num = max(page_num, int(match_data[-1]))


def run(conf_file) :
	conf_json = jt.load_conf(conf_file)
	total_page_num = fetch_tv_total_page(conf_json)
	logger.info("Total page number of IQIYI is : {}".format(total_page_num))
