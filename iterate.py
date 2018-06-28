from classes.sampify import Sampify
from classes.naf import naf
from classes.counter import countEmotions, countSampa
from config import *
import json, xlrd, xlwt

def read_xls(s):
    debug.debug("reading text-related settings")
    wb = xlrd.open_workbook(s['TEXTSETTINGS'])
    sh = wb.sheet_by_name('Sheet1')
    result=[{sh.row_values(0)[i]:sh.row_values(j)[i] for i in range(len(sh.row_values(0)))} for j in range(1,sh.nrows)]
    for i in result:
        i.update({'OUT': s['OUTPATH']+'/'+i['NAF'].split('/')[-1][:-3] + 'count.json'})
    return result

def make_dict(s):
    debug.debug("building dictionaries")
    dictionaries={}
    for i in s['RULES']:
        debug.debug("adding dictionary {0}".format(i))
        dictionaries[i]=Sampify(s['RULES'][i])
        dictionaries[i]._write_json(s['RULES'][i]+'.json')
    return dictionaries

def build_text(s,dictionaries):
    stdout.info("parsing {0}".format(s['NAME']))
    debug.debug("parsing {0}".format(s['NAME']))
    debug.debug("using emotion threshold: {0}".format(s['EMOTION THRESHOLD']))
    n = naf(s['NAF'],s['EMOTION THRESHOLD'])
    debug.debug("using dictionary {0}".format(s['DICTIONARY']))
    stdout.info("translating {0}".format(s['NAME']))
    n.translate(dictionaries[s['DICTIONARY']])
    stdout.info("counting {0}".format(s['NAME']))
    n.doCount()
    return n

def save_text(s,text, emotions, clusters):
    debug.debug("saving {0}".format(s['OUT']))
    stdout.info("saving {0}".format(s['OUT']))

    result={'sampa count':   text.countSampa.sampaCount(),
            'emotion count': text.countEmotions.emotionCount(),
            'cluster count': text.countEmotions.clusterCount(),
            'sampa count per cluster': clusters,
            'sampa count per emotion': emotions}

    with open(s['OUT'],'w') as f:
        json.dump(result, f, indent=4)

def save_result(f, text):
    debug.debug("writing to excel")
    wb = xlwt.Workbook()
    sh = wb.add_sheet("Sheet1")
    line=1
    for i in text:
        sh.write(line,0,i)
        col=1
        result=text[i].countSampa.sampaCount()
        tot_Sampa = 0
        for j in result:
            if line==1: sh.write(0, col, j)
            sh.write(line, col, result[j])
            col+=1
            tot_Sampa+=result[j]
        if line == 1: sh.write(0, col, 'sampa total')
        sh.write(line, col, tot_Sampa)
        col+=1

        result = text[i].countEmotions.emotionCount()
        tot_Emo=0
        for j in result:
            if line==1: sh.write(0, col, j)
            sh.write(line, col, result[j])
            col+=1
            tot_Emo+=result[j]
        if line == 1: sh.write(0, col, 'emotions total')
        sh.write(line, col, tot_Emo)
        col+=1

        result=text[i].countEmotions.clusterCount()
        tot_Clust=0
        for j in result:
            if line==1: sh.write(0, col, 'cluster:'+j)
            sh.write(line, col, result[j])
            col+=1
            tot_Clust+=result[j]
        if line == 1: sh.write(0, col, 'clsuters total')
        sh.write(line, col, tot_Clust)
        col+=1

        line += 1
    wb.save(f)

if __name__ == "__main__":
    debug = logging.getLogger('debugLog')
    stdout = logging.getLogger('stdoutLog')

    # build all dictionaries
    stdout.info('reading dictionaries')
    dictionaries=make_dict(globalSettings)

    # get settings for texts
    stdout.info('reading text settings')
    textSettings = read_xls(globalSettings)

    # make the run a bit shorter by looping over 1 text only
    # textSettings=[textSettings[0]]

    # read settings for a text
    result={}
    for i in textSettings:
        # make naf object
        stdout.info('starting text {0}/{1}'.format(1+textSettings.index(i),len(textSettings)))
        text=build_text(i,dictionaries)
        result[i['NAME']]=text

        sampacount_per_emotion={i:countSampa() for i in countEmotions().emotions}
        sampacount_per_cluster={i:countSampa() for i in countEmotions().clusters}

        for k in text.WordList:
            if k.EmotionList()!= None and len(k.EmotionList().Emotion())>0 and k.Sampa()!= None:
                for j in k.EmotionList().Emotion():
                    if j.Reference() in sampacount_per_emotion:
                        sampacount_per_emotion[j.Reference()].add(k.Sampa())
            if k.EmotionList() != None and len(k.EmotionList().Cluster()) > 0 and k.Sampa() != None:
                for j in k.EmotionList().Cluster():
                    if j.Reference() in sampacount_per_cluster:
                        sampacount_per_cluster[j.Reference()].add(k.Sampa())

        # save result of naf object
        sampacount_per_cluster={i:sampacount_per_cluster[i].sampaCount() for i in sampacount_per_cluster}
        sampacount_per_emotion={i:sampacount_per_emotion[i].sampaCount() for i in sampacount_per_emotion}

        save_text(i,text, sampacount_per_emotion, sampacount_per_cluster)

    stdout.info('saving counts to {0}'.format(globalSettings['COUNTS']))
    save_result(globalSettings['COUNTS'], result)
