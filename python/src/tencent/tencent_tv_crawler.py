import sys
import codecs
import re
sys.path.append("..")
import tools.NetworkTools as nt
import tools.json_tools as jt
from tools.logger_tool import *
from optparse import OptionParser


def fetch_tv_total_page(conf_json) :
    content = nt.fetchUrlContent(conf_json["url"])
    pattern = re.compile(conf_json["tv_total_page_pattern"])
    match_data = re.search(pattern, content)
    if match_data != None :
        return int(match_data.group(1))
    return 0

def fetch_tv_url_list(conf_json) :
    

def run(conf_file) :
    conf_json = jt.load_conf(conf_file)
    total_page_num = fetch_tv_total_page(conf_json)
    print 'total_page_num : {}'.format(total_page_num)
