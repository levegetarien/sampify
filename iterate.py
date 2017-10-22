from classes.sampify import Sampify
from classes.naf import naf
from config import *
import json, xlrd
from datetime import datetime as date

def read_xls(x):
    log.info("reading text-related settings")
    wb = xlrd.open_workbook(x)
    sh = wb.sheet_by_name('Sheet1')
    return [{sh.row_values(0)[i]:sh.row_values(j)[i] for i in range(len(sh.row_values(0)))} for j in range(1,sh.nrows)]

def make_dictionaries(s):
    log.info("building dictionaries")
    dictionaries={}
    for i in s['RULES']:
        log.info("adding dictionary {0}".format(i))
        dictionaries[i]=Sampify(s['RULES'][i])
    return dictionaries

def build_text(s,dictionaries):
    log.info("parsing {0}".format(s['NAME']))
    log.info("using emotion threshold: {0}".format(s['EMOTION THRESHOLD']))
    stdout.debug('reading NAF')
    n = naf(s['NAF'],s['EMOTION THRESHOLD'])
    log.info("using dictionary {0}".format(s['DICTIONARY']))
    stdout.debug('translating')
    n.translate(dictionaries[s['DICTIONARY']])
    stdout.info('counting')
    n.doCount()
    return n

def save_text(s,text):
    log.info("saving {0}".format(i['NAME']))
    with open(s['OUT'],'w') as f:
        json.dump(text.countSampa.sampaCount(), f, indent=4)
        json.dump(text.countEmotions.emotionCount(), f, indent=4)
        json.dump(text.countEmotions.clusterCount(), f, indent=4)

if __name__ == "__main__":
    log = logging.getLogger('sampify')
    stdout = logging.getLogger('stdout')
    # build all dictionaries
    stdout.debug('reading dictionaries')
    dictionaries=make_dictionaries(globalSettings)

    # get settings for texts
    stdout.debug('reading text settings')
    textSettings = read_xls(globalSettings['textSettings'])

    # read settings for a text
    for i in textSettings:
        # make naf object
        stdout.debug('reading text {0}'.format(i['NAME']))
        text=build_text(i,dictionaries)
        # save result of naf object
        stdout.debug('saving text {0}'.format(i['NAME']))
        save_text(i,text)
