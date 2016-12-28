import sys, glob, logging
sys.path.append(glob.glob('/Users/*/Dropbox/sampify')[0])
from libs.dictionary import *

logger = logging.getLogger('sampify')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('log_dictionary_test.txt')
fh2= logging.FileHandler('wrn_dictionary_test.txt')
fh.setLevel(logging.DEBUG)
fh2.setLevel(logging.WARN)
fh.setFormatter(logging.Formatter( '[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s', "%Y-%m-%d %H:%M:%S"))
fh2.setFormatter(logging.Formatter('[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s', "%Y-%m-%d %H:%M:%S"))
logger.addHandler(fh)
logger.addHandler(fh2)

D=Dictionary()
D.add_list_fromfile('inp_dictionary_test.txt')
D.add_word_i("testwoord1")
D.add_word_a("testwoord2","SAMPAwoord2")
D.save_dict('out_dictionary_test.txt')
