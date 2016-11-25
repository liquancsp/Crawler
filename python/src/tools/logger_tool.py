import logging
import logging.config

class Logger :
	def __init__(self) :
		logging.config.fileConfig("../../conf/logger.conf")
		self.logger = logging.getLogger()

	def getlog(self) :
		return self.logger

logger = Logger().getlog()
