import sys, glob, logging
sys.path.append(glob.glob('/Users/*/Dropbox/sampify')[0])
from libs.word       import *
from libs.dictionary import *

logger = logging.getLogger('sampify')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('log_word_test.txt')
fh2= logging.FileHandler('wrn_word_test.txt')
fh.setLevel(logging.DEBUG)
fh2.setLevel(logging.WARN)
fh.setFormatter(logging.Formatter( '[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s', "%Y-%m-%d %H:%M:%S"))
fh2.setFormatter(logging.Formatter('[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s', "%Y-%m-%d %H:%M:%S"))
logger.addHandler(fh)
logger.addHandler(fh2)

#to be written when class is fully rstructured!
