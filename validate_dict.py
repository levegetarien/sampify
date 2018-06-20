from classes.sampify import Sampify
from config import *
import codecs

def test_dict_quality(ref,dictionary):
    TOT,NOK,result=0,0,''
    with codecs.open(ref, "r", encoding='utf-8') as f:
        for line in f:
            words=line.split()
            if len(words)>1:
                TOT+=1
                NL,REF  =words[0], words[1]
                VERT=dictionary.translate(NL)
                if REF!=VERT:
                    NOK+=1
                    result+="{0:<25}\t{1:<25}\t{2:<25}\n".format(NL,REF,VERT)
    print('error percentage: {0}% ({1} of {2} words)'.format(int(NOK*100/(TOT)),NOK,TOT))
    return result

if __name__ == "__main__":
    RULES='/Users/ruben/Projects/Sampify/files/in/RULES_A_V1.5.xlsx'
    REF="/Users/ruben/Projects/Sampify/files/in/referentie_vertaling_grpA_v1.5.txt"
    ERRORS="/Users/ruben/Projects/Sampify/files/out/validatie_rules1.5_ref1.5.txt"

    debugLog.setLevel(logging.DEBUG)

    '''
    LOGS="/Users/ruben/Projects/Sampify/files/out/logs_wordlist_rulesV1.5.txt"
    addStreamToLogger(debugLog, file=LOGS, level=logging.DEBUG)

    dictionary=Sampify(RULES)
    wordlist=[
        "aanstootelyks",
        "collationeeren",
        "conjungeren",
        "discurreeren",
        "drooghals",
        "gerequireerdens",
        "irreprochabel",
        "onnoosle",
        "pleidoyeeren"
    ]
    for NL in wordlist:
        dictionary.translate(NL)
    '''

    with codecs.open(ERRORS,'w', encoding='utf-8') as g:
        g.write(test_dict_quality(REF,Sampify(RULES)))
