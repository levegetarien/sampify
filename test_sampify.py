from classes.sampify import Sampify
from classes.naf import naf
from classes.sampa_counter import count
from config import *

a=Sampify(PATH+'/files/in/RULES werkdocument.xlsx')
n=naf(PATH+'/files/in/naf_alew001besl01_01.xml')
c=count()
words_nl=n.get_wordlist_nopunct()
words_sp=[a.translate(i) for i in words_nl]
for i in range(len(words_nl)):
    c.add(words_sp[i])
    print(words_nl[i],words_sp[i])
print(c.count)

with open(PATH+'/files/in/lijst_Alewijn_corrected_t_m_q.txt') as data_file:
    content = [x.strip() for x in data_file.readlines()]
    newtable_good=""
    newtable_baad=""
    for i in content:
        if len(i)>1:
            nl=i.split()[0]
            smpa = i.split()[-1]
            if smpa == a.translate(nl):
                newtable_good += "{0:<20}\t{1:<20}\n".format(nl, a.translate(nl))
            if smpa != a.translate(nl):
                newtable_baad += "{0:<20}\t{1:<20}\t{2:<20}\n".format(nl, smpa, a.translate(nl))

with open(PATH+'/files/out/lijst_Alewijn_sampified_good.txt','w') as g: g.write(newtable_good)
with open(PATH+'/files/out/lijst_Alewijn_sampified_bad.txt','w') as g: g.write(newtable_baad)

"""
a=rules()
a.add_rules(fromfile='rules.xlsx')
a._write_json('test1.json')
b=rules()
b.add_rules(fromfile='rules4.csv')
b._write_json('test2.json')
"""
"""
a=rules()
a.add_rules('rules.json')
a.add_rules('rules.csv')
a.add_rules(fromline=True)
print(a.rules['V']['y']['default'])
"""
"""
a=make_sampa()
a.add_rules('rules.json')
a.rules['V']['aa']=a.rules["V"].pop('a')
a.rules.pop('P')
print(a.rules)
a._quality_check(a.rules)
"""
"""
a._write_json('test.json')
for i in ['boocabt','boocaboo','boocab']: print("{0:<10} --> {1}".format(i,a.sampify(i)))
"""
"""
#b=make_sampa('/Users/*/Dropbox/sampify_autom_rules_test/rules.csv')
#b.write_json('/Users/*/Dropbox/sampify_autom_rules_test/rules_from_csv_2.json')
#for i in ['baco']: print("{0:<10} --> {1}".format(i,b.sampify(i)))
"""