from classes.counter import countSampa,compare
from classes.sampify import Sampify
from classes.naf import naf
from config import *
import codecs

def read_naf():
    a = Sampify(FILES['RULES'])
    n = naf(FILES['NAF'],SETTINGS['EMOTION THRESHOLD'])
    n.translate(a)

    for i in n.WordList:
        if i.isNotPunctuation():
            print(i.Word(),i.Sampa())

def validate():
    a = Sampify(FILES['RULES'])
    c_ref = countSampa()
    c_trans = countSampa()
    with codecs.open(PATH + '/files/in/lijst_Alewijn_corrected.txt', 'r', encoding='UTF-8') as data_file:
        content = [x.strip() for x in data_file.readlines()]
        new_table_good, new_table_baad = "", ""
        for i in content:
            if len(i) > 1:
                nl = i.split()[0]
                smpa = i.split()[-1]
                c_ref.add(smpa)
                c_trans.add(a.translate(nl))

                if smpa == a.translate(nl): new_table_good += "{0:<20}\t{1:<20}\n".format(nl, a.translate(nl))
                if smpa != a.translate(nl): new_table_baad += "{0:<20}\t{1:<20}\t{2:<20}\n".format(nl, smpa, a.translate(nl))

    c=compare(c_ref)
    print_errors(c_ref,c_trans,c.all,"alle letters")
    print_errors(c_ref,c_trans,c.vowels,"alle klinkers")
    print_errors(c_ref,c_trans,c.consonnants,"alle medeklinkers")
    print_errors(c_ref,c_trans,c.fricatives,"alle fricativen")
    print_errors(c_ref,c_trans,c.plosives,"alle plosiven")
    print_errors(c_ref,c_trans,c.sonorants,"alle sonoranten")
    print_errors(c_ref,c_trans,c.checked,"alle gesloten")
    print_errors(c_ref,c_trans,c.potential_diphthongs,"alle potentiele diphtongen")
    print_errors(c_ref,c_trans,c.essential_diphthongs,"alle essentiele diphtongen")
    print_errors(c_ref,c_trans,c.others,"alle andere klinkers")

    return new_table_good, new_table_baad

def print_errors(c_ref,test,group,name):
    a = compare(c_ref)
    a.add(test,group)
    bad,tot=a.get_score()
    print("{0:<40}\t errors:{1:7.2f}%\t (N={2:5d})".format(name,float(bad/tot)*100,tot))
    del a



if __name__ == "__main__":
    read_naf()
    # words, count = read_naf()
    # for i in words:
    #     print("{0:<20}\t{1:<20}".format(i[0], i[1]))
    # for i in count.keys():
    #     print("{0:<20}\t{1:<20}".format(i, count[i]))

    # good,bad=validate()
    # with open(PATH+'/files/out/lijst_Alewijn_sampified_good.txt','w') as g: g.write(good)
    # with open(PATH+'/files/out/lijst_Alewijn_sampified_bad.txt','w') as g: g.write(bad)
