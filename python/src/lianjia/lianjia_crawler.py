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

def fetch_total_page(conf_json) :
	content = nt.fetchUrlContent(conf_json["url"])
	pattern = re.compile(conf_json["tv_total_page_pattern"])
	match_data = re.search(pattern, content)
	if match_data != None :
		return int(match_data.group(1))
	return 0

def fetch_house_info(conf_json, total_num) :
	house_info_csv = file(conf_json["house_info_file"]["file_name"], 'wb')
	write = csv.writer(house_info_csv)
	write.writerow(conf_json["house_info_file"]["column_name"].split(','))
	cnt = 0
	for page_no in range(total_num) :
		for i in range(int(conf_json["retry_times"])) :
			#format tv show real url
			url = conf_json["list_template_url"].format(page_no + 1)
			timeout = int(conf_json["timeout"])
			print 'Begin fetch : {}'.format(url)
			content = nt.fetchUrlContent(url, timeout)
			if content != None :
				content = content.replace('\n', '').replace('\t', '').replace('\t', '')
				pattern = re.compile(conf_json["house_info_pattern"])
				match_data = re.findall(pattern, content)
				if match_data == None :
					logger.error('Bad format for url content : {}'.format(url))
					break;
				print match_data
				# write.writerows(match_data)
				cnt = cnt + len(match_data)
				break

def run(conf_file) :
    conf_json = jt.load_conf(conf_file)
    total_page_num = fetch_total_page(conf_json)
    logger.info('total_page_num : {}'.format(total_page_num))
    print 'total_page_num : {}'.format(total_page_num)
    fetch_house_info(conf_json, total_page_num)

if __name__ == "__main__" :
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage = usage)
    parser.add_option("-c", "--conf",  action = "store", type = "string",
        dest = "conf_file",  help="It is the config file for the crawler.")
    (options, args) = parser.parse_args()
    run(options.conf_file)