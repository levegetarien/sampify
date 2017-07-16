from classes.sampa_counter import count,compare
from classes.sampify import Sampify
from classes.naf import naf
from config import *
import codecs

def read_naf():
    a = Sampify(PATH + '/files/in/RULES werkdocument.xlsx')
    n = naf(PATH + '/files/in/naf_alew001besl01_01.xml')
    c = count()

    words_nl = n.get_wordlist_nopunct()
    words_sp = [a.translate(i) for i in words_nl]
    words_tpl= zip(words_nl, words_sp)
    for i in words_sp: c.add(i)

    return words_tpl, c.count


def validate():
    a = Sampify(PATH + '/files/in/RULES werkdocument.xlsx')
    c_ref = count()
    c_trans = count()
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
    # words, count = read_naf()
    # for i in words:
    #     print("{0:<20}\t{1:<20}".format(i[0], i[1]))
    # for i in count.keys():
    #     print("{0:<20}\t{1:<20}".format(i, count[i]))

    good,bad=validate()
    # with open(PATH+'/files/out/lijst_Alewijn_sampified_good.txt','w') as g: g.write(good)
    # with open(PATH+'/files/out/lijst_Alewijn_sampified_bad.txt','w') as g: g.write(bad)
