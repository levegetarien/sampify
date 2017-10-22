import logging,sys

# global settings
globalSettings={
    'RULES': {
        'RULES A': '/Users/ruben/Projects/Sampify/files/RULES werkdocument.xlsx',
        'RULES B': '/Users/ruben/Projects/Sampify/files/RULES werkdocument.xlsx',
        'RULES C': '/Users/ruben/Projects/Sampify/files/RULES werkdocument.xlsx',
        'RULES D': '/Users/ruben/Projects/Sampify/files/RULES werkdocument.xlsx'
    },
    'LOGGER': 'sampify',
    'PATH': '/Users/ruben/Projects/Sampify',
    'LOG': '/Users/ruben/Projects/Sampify/files/log/log_dictionary_test.txt',
    'WRN': '/Users/ruben/Projects/Sampify/files/log/wrn_dictionary_test.txt',
    'textSettings':'/Users/ruben/Projects/Sampify/files/Toneel_settings.xlsx'
}


logger = logging.getLogger(globalSettings['LOGGER'])
logger.setLevel(logging.DEBUG)

fh1 = logging.FileHandler(globalSettings['LOG'],encoding='utf-8')
fh2 = logging.FileHandler(globalSettings['WRN'],encoding='utf-8')
fh1.setLevel(logging.DEBUG)
fh2.setLevel(logging.WARN)
fh1.setFormatter(
    logging.Formatter(u'[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s',
                      "%Y-%m-%d %H:%M:%S"))
fh2.setFormatter(
    logging.Formatter(u'[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s',
                      "%Y-%m-%d %H:%M:%S"))
logger.addHandler(fh1)
logger.addHandler(fh2)

stdoutlogger = logging.getLogger('stdout')
stdoutlogger.setLevel(logging.DEBUG)

sh = logging.StreamHandler(sys.stdout)
sh.setLevel((logging.DEBUG))
sh.setFormatter(
    logging.Formatter(u'[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s',
                      "%Y-%m-%d %H:%M:%S"))
stdoutlogger.addHandler(sh)


