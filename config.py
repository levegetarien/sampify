import logging

PATH="/Users/cvr270/PycharmProjects/sampify/"


logger = logging.getLogger('sampify')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(PATH + '/files/log/log_dictionary_test.txt')
fh2 = logging.FileHandler(PATH + '/files/log/wrn_dictionary_test.txt')
fh.setLevel(logging.DEBUG)
fh2.setLevel(logging.WARN)
fh.setFormatter(
    logging.Formatter('[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s',
                      "%Y-%m-%d %H:%M:%S"))
fh2.setFormatter(
    logging.Formatter('[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s',
                      "%Y-%m-%d %H:%M:%S"))
logger.addHandler(fh)
logger.addHandler(fh2)