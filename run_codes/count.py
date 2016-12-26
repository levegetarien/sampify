#!/usr/bin/python

#########################################################################################
#    HIER OMPORTEREN WE ONZE LIBRARIES; IN DIE LIBRARIES WORDT HET MEESTE WERK GEDAAN   #
#########################################################################################

from LIBS.classes_V4 import *
from SETTINGS.paths import *
from SETTINGS.count_settings_alew_001besl01_01 import *

#some file locations

lidwoorden      = files["lidwoorden"]
voornaamwoorden = files["voornaamwoorden"]
prefixen        = files["prefixen"]
suffixen        = files["suffixen"]
sampletekst1     = files["xml"]
#sampletekst     = files["text"]
indictionary    = files["indictionary"]
outdictionary   = files["outdictionary"]
output          = files["output"]
plaatje         = files["graph"]
lemma           = files["lemma"]

from SETTINGS.count_settings_noms001mich01_01 import *
sampletekst2     = files["xml"]

from SETTINGS.count_settings_vond001gysb01_01 import *
sampletekst3     = files["xml"]


class Dictionary_met_count(Dictionary):
  def add_word_a(self,W,N):
    if W in self.sampa.keys():
      self.sampa[W]+=1
      self.log.info("word \"{0}\" already in dictionary, current count: \"{1}\"".format(W,self.sampa[W]))
    else: 
      self.sampa[W]=1
      self.log.info("word \"{0}\" added to dictionary,   count set to:  \"{1}\"".format(W,self.sampa[W]))
  def save_dict2(self,outf):
    a=[]
    for i in self.sampa.keys():
      a.append((i,self.sampa[i]))
    b= sorted(a, key=lambda tup: tup[1], reverse=True)
    with open(outf, "w") as g:
      c=0
      for i in b:
        c+=1
        g.write("{0: <30} {1: <30} {2: <30}\n".format(c,i[0],i[1]))
    self.log.info("Dictionary saved to file {0}".format(outf))
  
class Word2(Word):
  def sampa(self):
    if len(self.attr["clean"])>0:
      self.dictionary.add_word_a(self.attr["clean"],0)
class Text2(Text):    
  def translate(self):
    self.fulltext_e=[Word2(i, self.log, self.preflist, self.suflist,self.dictionary,self.lemmalist,self.punctuation) for i in self.fulltext_o]

#########################################################################################

#########################################################################################
#     DIT IS DE ECHTE CODE, HIERBOVEN HEBBEN WE ALLEEN MAAR DEFINITIES OPGESCHREVEN     #
#########################################################################################

#maak een lege tekst aan
T=Text2(logger, prefixen, suffixen,Dictionary_met_count(logger),lemma)
T.add_text_fromxml(sampletekst1)
T.add_text_fromxml(sampletekst2)
T.add_text_fromxml(sampletekst3)
T.translate()
T.dictionary.save_dict2(outdictionary)
