import sys
sys.path.append("..")
import tools.NetworkTools as nt
import tools.json_tools as jt


def run(conf_file) :
    conf = jt.load_conf(conf_file)
    content = nt.fetchUrlContent(conf["url"])
