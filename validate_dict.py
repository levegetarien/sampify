from classes.sampify import Sampify
from classes.naf import naf
from config import *
import json, xlrd, codecs

if __name__ == "__main__":
    debug = logging.getLogger('debugLog')
    stdout = logging.getLogger('stdoutLog')

    # build all dictionaries
    dictionary=Sampify('/Users/ruben/Projects/Sampify/files/in/RULES_A_V1.1.xlsx')
    # print(dictionary.translate('test'))
    OK,NOK=0,0
    g=codecs.open("/Users/ruben/Projects/Sampify/files/out/validatie.txt",'w', encoding='utf-8')
    with codecs.open("/Users/ruben/Projects/Sampify/files/in/referentie_vertaling_grpA.txt", "r", encoding='utf-8') as f:
        for line in f:
            words=line.split()
            if len(words)>1:
                NL  =words[0]
                REF =words[1]
                VERT=dictionary.translate(NL)
                if REF!=VERT:
                    NOK+=1
                    g.write("{0:<30}{1:<30}{2:<30}\n".format(NL,REF,VERT))
                else:
                    OK+=1
    g.close()
    print(NOK,OK)
