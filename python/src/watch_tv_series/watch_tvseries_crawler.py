import sys
import codecs
import re
sys.path.append("..")
import tools.network_tool as nt
import tools.json_tools as jt
from tools.logger_tool import *
from optparse import OptionParser


def fetch_tv_url_list(conf) :
    content = nt.fetchUrlContent(conf["url"])
    pattern = re.compile(conf["tv_list_pattern"])
    match_data = re.findall(pattern, content)
    return match_data

def fetch_episode_info(conf, tv_url_list) :
    logger.info("Begin to fetch_episode_info")
    result_file = codecs.open(conf["eps_info_file"], 'w', 'utf-8')
    for tv_info in iter(tv_url_list) :
        tv_episode_pattern = re.compile(conf["tv_episode_pattern"])
        episode_org_img_pattern = re.compile(r'a title="(.*?)"\s+href="(.*?)">.*?data-original="([^"]+)')
        episode_src_img_pattern = re.compile(r'a title="(.*?)"\s+href="(.*?)">.*?src="([^"]+)')
        tailer_url = tv_info[0]
        if tailer_url.startswith('/') == False :
            tailer_url = '/' + tv_info[0]
        tv_home_base_url = conf["home_base_url"]
        episode_url = tv_home_base_url + tailer_url
        for i in range(int(conf["retry_times"])) :
            episode_page_content = nt.fetchUrlContent(episode_url)
            if episode_page_content != None :
                eps_match = re.findall(tv_episode_pattern, episode_page_content)
                for eps_detail in iter(eps_match) :
                    match = episode_org_img_pattern.search(eps_detail)
                    if match == None:
                        match = episode_src_img_pattern.search(eps_detail)
                    if match == None:
                        logger.error('Vaild eps_detail : {}'.format(eps_detail))
                        continue
                    eps_title = match.group(1)
                    eps_tailer_url = match.group(2)
                    eps_img_url = match.group(3)
                    if eps_tailer_url is not None and eps_title is not None :
                        eps_season_info = eps_tailer_url.split('/')[3].split('-')
                        if len(eps_season_info) < 5 :
                            logger.error('Bad url format : {}'.format(eps_tailer_url))
                            continue
                        season_number = int(eps_season_info[1])
                        eps_number = int(eps_season_info[3])
                        try :
                            result_file.write('{}\t{}\t{}\t{}\t{}\t{}\n'.format(tv_info[1], season_number,
                             eps_number, tv_home_base_url + eps_tailer_url, eps_title, eps_img_url))
                        except Exception, msg:
                            logger.error('Write file excetion {} : {}'.format(msg, eps_detail))

                break
            time.sleep(5)
    result_file.close()

def run(conf_file) :
    conf_json = jt.load_conf(conf_file)
    tv_list = fetch_tv_url_list(conf_json)
    fetch_episode_info(conf_json, tv_list)

if __name__ == "__main__" :
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage = usage)
    parser.add_option("-c", "--conf",  action = "store", type = "string",
        dest = "conf_file",  help="It is the config file for the crawler.")
    (options, args) = parser.parse_args()
    run(options.conf_file)
