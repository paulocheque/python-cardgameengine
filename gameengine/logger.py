'''
@author: Paulo Cheque (paulocheque@gmail.com)
'''

# http://docs.python.org/library/logging.html
import logging

LOG_FILENAME = '/tmp/gat.log'
logger = logging.getLogger("game")
logger.setLevel(logging.DEBUG)
#logger.setLevel(logging.WARN)

consoleHandler = logging.StreamHandler()
#consoleHandler.setLevel(logging.DEBUG)
consoleHandler.setLevel(logging.INFO)
logger.addHandler(consoleHandler)

#TimedRotatingFileHandler
#fileHandler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=20, backupCount=5)
#fileHandler.setLevel(logging.DEBUG)
#fileHandler.setLevel(logging.INFO)
#logger.addHandler(fileHandler)

