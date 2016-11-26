import urllib2
import sys
import traceback
import socket
import re
from logger_tool import *

def fetchUrlContent(url, timeout = 5) :
	headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
	request = urllib2.Request(url=url, headers=headers)
	content = None
	socket_res = None
	try :
		socket_res = urllib2.urlopen(request, timeout=timeout)
		content = socket_res.read()
	except Exception, e:
		logger.error('socket timeout for {}, {}'.format(url, e))
		return None
	finally :
		if socket_res != None :
			socket_res.close()
	return content
