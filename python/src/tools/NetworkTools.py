import urllib2
import sys 
import traceback

def fetchUrlContent(url, timeout = 5) :
	headers = {'User-Agent':'Mozilla/5.0 (X11; U; Linux i686)Gecko/20071127 Firefox/2.0.0.11'}
	request = urllib2.Request(url=url, headers=headers)
	try :
		socket = urllib2.urlopen(request, timeout=timeout)
	except urllib2.URLError, e:
		print "Request url error!"
		traceback.print_exc(file=sys.stdout)
		return None
	content = socket.read();
	socket.close()
	return content
		

