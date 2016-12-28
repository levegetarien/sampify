import sys, glob, logging
sys.path.append(glob.glob('/Users/*/Dropbox/sampify')[0])
from libs.sampa_vowels import *

logger = logging.getLogger('sampify')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('log_sampa_vowels_test.txt')
fh2= logging.FileHandler('wrn_sampa_vowels_test.txt')
fh.setLevel(logging.DEBUG)
fh2.setLevel(logging.WARN)
fh.setFormatter(logging.Formatter( '[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s', "%Y-%m-%d %H:%M:%S"))
fh2.setFormatter(logging.Formatter('[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s', "%Y-%m-%d %H:%M:%S"))
logger.addHandler(fh)
logger.addHandler(fh2)


with open('inp_sampa_vowels_test.txt','r') as f:
    for line in f:
        if len(line.split())>1:
            w=line.split()[1]
            S=SampaV(w)
            print 'source:   ', w
            print 'count:    ', S.vowels
            print 'non-zero: ', S.printused()
