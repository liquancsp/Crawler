import sys
import codecs
import re
import csv
import urllib2
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

# parameter :
# conf_json : An json object that store all config infornmation.
# total_num : The number of TV show list pages.
#
# Save all the TV show infornmations into csv file which path define in configure
# file(tv_show_file)
#
def fetch_tv_url_list(conf_json, total_num) :
    tv_show_csv = file(conf_json["tv_show_file"]["file_name"], 'wb')
    write = csv.writer(tv_show_csv)
    write.writerow(conf_json["tv_show_file"]["column_name"].split(','))
    cnt = 0;
    for page_no in range(total_num) :
        for i in range(int(conf_json["retry_times"])) :
            #format tv show real url
            tv_list_url = conf_json["tv_list_template_url"].format(page_no * 20)
            # get http page content and replace \n \t  to ''
            timeout = int(conf_json["timeout"])
            content = nt.fetchUrlContent(tv_list_url, timeout).replace('\n', '').replace('\t', '')
            if content != None :
                pattern = re.compile(conf_json["tv_show_pattern"])
                # match all pattern return a list of all result
                match_data = re.findall(pattern, content)
                if match_data == None :
                    logger.error('Bad format for url content : {}'.format(tv_list_url))
                    break
                write.writerows(match_data)
                cnt = cnt + len(match_data)
                break
            time.sleep(5)
    logger.info('Total tv show is : {}'.format(cnt))
    if cnt != 0 :
        return True
    else :
        return False

#
#parameter : 
#conf_json : An json object that store all configure information
#
# Read the tv show list from tv_show_list file. And for each tvshow request it's episode information.
# And save it to tv_episode_file which path define in conf file
#
def fetch_episode_info(conf_json) :
    with open(conf_json["tv_show_file"]["file_name"], "r") as csvfile:
        reader =  csv.reader(csvfile, delimiter=",")
        pattern = re.compile(conf_json['tv_episode_pattern'])
        reader.next()
        with open(conf_json["tv_episode_file"]["file_name"], "w") as writefile :
            writer = csv.writer(writefile)
            writer.writerow(conf_json["tv_episode_file"]["column_name"].split(','))
            timeout = int(conf_json["timeout"])
            eps_cnt = 0
            for url, img, title, count in reader :
                real_url = conf_json['redirct_base_url'] + url.split('/')[-1]
                for i in range(int(conf_json['retry_times'])) :
                    content = nt.fetchUrlContent(real_url, timeout).replace('\n', '').replace('\t', '')
                    if content != None :
                        match = re.findall(pattern, content)
                        if match :
                            writer.writerows(match)
                            eps_cnt = eps_cnt + len(match)
                        else :
                            logger.error('bad format for : {}'.format(real_url))
                        break
            logger.info('The number of episode is : {}'.format(eps_cnt))

def run(conf_file) :
    conf_json = jt.load_conf(conf_file)
    total_page_num = fetch_tv_total_page(conf_json)
    logger.info('total_page_num : {}'.format(total_page_num))
    is_success = fetch_tv_url_list(conf_json, total_page_num)
    if is_success == True :
        fetch_episode_info(conf_json)

if __name__ == "__main__" :
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage = usage)
    parser.add_option("-c", "--conf",  action = "store", type = "string",
        dest = "conf_file",  help="It is the config file for the crawler.")
    (options, args) = parser.parse_args()
    run(options.conf_file)
