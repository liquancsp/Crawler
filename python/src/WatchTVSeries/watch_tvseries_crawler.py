import sys
import re
sys.path.append("..")
import tools.NetworkTools as nt
import tools.json_tools as jt


def fetch_tv_url_list(conf_file) :
    conf = jt.load_conf(conf_file)
    content = nt.fetchUrlContent(conf["url"])
    pattern = re.compile(conf["tv_list_pattern"])
    match_data = re.findall(pattern, content) 
    return match_data

def fetch_episode_info(conf_file, tv_url_list) :
    conf = jt.load_conf(conf_file)
    cnt = 0
    exp_file = file(conf["exception_file_path"], "w+")
    for tv_info in iter(tv_url_list) :
	if cnt == 2 :
            break
        tv_episode_pattern = re.compile(conf["tv_episode_pattern"])
	episode_org_img_pattern = re.compile(r'a title="(.*?)"\s+href="(.*?)">.*?data-original="([^"]+)')
	episode_src_img_pattern = re.compile(r'a title="(.*?)"\s+href="(.*?)">.*?src="([^"]+)')
        tailer_url = tv_info[0]
	if tailer_url.startswith('/') == False :
            tailer_url = '/' + tv_info[0]
        episode_url = conf["home_base_url"] + tailer_url
	print 'episode_url {}'.format(episode_url)
        for i in range(int(conf["retry_times"])) :
            episode_page_content =  nt.fetchUrlContent(episode_url)
            if episode_page_content != None :
		eps_match = re.findall(tv_episode_pattern, episode_page_content)
		for eps_detail in iter(eps_match) :
		    match = episode_org_img_pattern.search(eps_detail)
		    if match == None:
			match = episode_src_img_pattern.search(eps_detail)
                    if match == None:
			exp_file.writeline('Vaild eps_detail : {}'.format(eps_detail))
		    print match.groups()

                break
    exp_file.close();	

