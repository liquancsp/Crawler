import urllib2
import sys 
import traceback
import socket

def fetchUrlContent(url, timeout = 5) :
	headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
	request = urllib2.Request(url=url, headers=headers)
	try :
		socket_res = urllib2.urlopen(request, timeout=timeout)
	except urllib2.URLError as e:
		print "Request url error!"
		traceback.print_exc(file=sys.stdout)
		return None
	except socket.timeout as e :
		print 'socket timeout for {}'.format(url)
		return None
	finally :
		socket_res.close()
	content = socket_res.read()
	return content
		

