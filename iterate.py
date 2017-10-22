from classes.sampify import Sampify
from classes.naf import naf
from config import *
import json, xlrd
from datetime import datetime as date

def read_xls(s):
    debug.debug("reading text-related settings")
    wb = xlrd.open_workbook(s['textSettings'])
    sh = wb.sheet_by_name('Sheet1')
    result=[{sh.row_values(0)[i]:sh.row_values(j)[i] for i in range(len(sh.row_values(0)))} for j in range(1,sh.nrows)]
    for i in result: i.update({'OUT': s['OUTPATH']+'/'+i['NAF'].split('/')[-1][:-3] + 'count.txt'})
    return result

def make_dict(s):
    debug.debug("building dictionaries")
    dictionaries={}
    for i in s['RULES']:
        debug.debug("adding dictionary {0}".format(i))
        dictionaries[i]=Sampify(s['RULES'][i])
    return dictionaries

def build_text(s,dictionaries):
    stdout.info('reading text {0}'.format(s['NAME']))
    debug.debug("parsing {0}".format(s['NAME']))
    debug.debug("using emotion threshold: {0}".format(s['EMOTION THRESHOLD']))
    stdout.info('reading NAF')
    n = naf(s['NAF'],s['EMOTION THRESHOLD'])
    debug.debug("using dictionary {0}".format(s['DICTIONARY']))
    stdout.info('translating')
    n.translate(dictionaries[s['DICTIONARY']])
    stdout.info('counting')
    n.doCount()
    return n

def save_text(s,text):
    debug.debug("saving {0}".format(i['NAME']))
    stdout.info("saving {0}".format(i['NAME']))
    with open(s['OUT'],'w') as f:
        json.dump(text.countSampa.sampaCount(), f, indent=4)
        json.dump(text.countEmotions.emotionCount(), f, indent=4)
        json.dump(text.countEmotions.clusterCount(), f, indent=4)

if __name__ == "__main__":
    debug = logging.getLogger('debugLog')
    stdout = logging.getLogger('stdoutLog')

    # build all dictionaries
    stdout.info('reading dictionaries')
    dictionaries=make_dict(globalSettings)

    # get settings for texts
    stdout.info('reading text settings')
    textSettings = read_xls(globalSettings)

    # read settings for a text
    for i in textSettings:
        # make naf object
        stdout.info('starting text {1}/{2}'.format(1+textSettings.index(i),len(textSettings)))
        text=build_text(i,dictionaries)
        # save result of naf object
        save_text(i,text)
