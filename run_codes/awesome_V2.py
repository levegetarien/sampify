#!/usr/bin/python

#########################################################################################
#    HIER OMPORTEREN WE ONZE LIBRARIES; IN DIE LIBRARIES WORDT HET MEESTE WERK GEDAAN   #
#########################################################################################

from LIBS.classes_V4 import *
from SETTINGS.paths import *
#from SETTINGS.settings_noms001mich01_01 import *
#from SETTINGS.settings_vond001gysb01_01 import *
from SETTINGS.run_6 import *

#some file locations

lidwoorden      = files["lidwoorden"]
voornaamwoorden = files["voornaamwoorden"]
prefixen        = files["prefixen"]
suffixen        = files["suffixen"]
sampletekst     = files["xml"]
#sampletekst     = files["text"]
indictionary    = files["indictionary"]
outdictionary   = files["outdictionary"]
output          = files["output"]
plaatje         = files["graph"]
lemma           = files["lemma"]

#########################################################################################
#     DIT IS DE ECHTE CODE, HIERBOVEN HEBBEN WE ALLEEN MAAR DEFINITIES OPGESCHREVEN     #
#########################################################################################
#maak een lege tekst aan
T=Text(logger, prefixen, suffixen,Dictionary(logger),lemma)
T.dictionary.add_list_fromfile(voornaamwoorden)
T.dictionary.add_list_fromfile(lidwoorden)
#T.dictionary.add_list_fromfile(indictionary)

#vul de tekst met de content van een bestand
#T.add_text_fromfile(sampletekst)
T.add_text_fromxml(sampletekst)
#zet de tekst om naar sampa
T.translate()

"""
T2=Dictionary(logger)
for i in T.fulltext_e: 
  if i.attr['act']==1 and i.attr['scene']==1:
    T2.add_word_a(i.attr['clean'],i.attr['sampa'])
T2.save_dict(outdictionary)
"""
"""
T.dictionary.save_dict(outdictionary)
"""
#for i in T.fulltext_e: print i.attr
#en laten we een telling doen
#laten we een lege teller maken
"""
ma={}
m1={}
m2={}
m3={}
for i in T.fulltext_e:  
  ma=count_vow(ma,i)
  if i.attr["act"]==1:  m1=count_vow(m1,i)
  if i.attr["act"]==2:  m2=count_vow(m2,i)
  if i.attr["act"]==3:  m3=count_vow(m3,i)
#plot_vow(m1)
plot_star_vow(m1,m2,m3, plaatje)
#en de totale score laten zien
#N.printcount(output)
#extra truukje: grafiekje
#N3.plotfig(plaatje)
"""
plot_heatmap(T.fulltext_e,PrintToFile=plaatje)