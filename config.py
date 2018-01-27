import logging,sys

# global settings
def addStreamToLogger(log,file=False,level=logging.DEBUG):
    stream = logging.StreamHandler(sys.stdout)
    if file: stream=logging.FileHandler(file,encoding='utf-8')
    stream.setLevel(level)
    stream.setFormatter(logging.Formatter(u'[%(asctime)s] [%(module)11s] [%(funcName)11s] [%(lineno)3s] [%(levelname)8s] - %(message)s',"%Y-%m-%d %H:%M:%S"))
    log.addHandler(stream)

globalSettings={
    'RULES': {
        'RULES A': '/Users/ruben/Projects/Sampify/files/in/RULES_A_V1.2.xlsx',
        'RULES B': '/Users/ruben/Projects/Sampify/files/in/RULES_A_V1.2.xlsx',
        'RULES C': '/Users/ruben/Projects/Sampify/files/in/RULES_A_V1.2.xlsx',
        'RULES D': '/Users/ruben/Projects/Sampify/files/in/RULES_A_V1.2.xlsx'
    },
    'PATH':        '/Users/ruben/Projects/Sampify',
    'OUTPATH':     '/Users/ruben/Projects/Sampify/files/out',
    'DEBUG':       '/Users/ruben/Projects/Sampify/files/log/debug_dictionary_test.txt',
    'WARNING':     '/Users/ruben/Projects/Sampify/files/log/warning_dictionary_test.txt',
    'TEXTSETTINGS':'/Users/ruben/Projects/Sampify/files/in/Toneel_settings.xlsx',
    'COUNTS':      '/Users/ruben/Projects/Sampify/files/out/count_per_play.xls'
}

debugLog = logging.getLogger('debugLog')
debugLog.setLevel(logging.WARNING)
# debugLog.setLevel(logging.DEBUG)

addStreamToLogger(debugLog,file=globalSettings['DEBUG'],level=logging.DEBUG)
addStreamToLogger(debugLog,file=globalSettings['WARNING'],level=logging.WARNING)

stdoutLog = logging.getLogger('stdoutLog')
stdoutLog.setLevel(logging.DEBUG)
addStreamToLogger(stdoutLog,level=logging.DEBUG)


