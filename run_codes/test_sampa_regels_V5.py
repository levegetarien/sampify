#!/usr/bin/python

#some imports
import glob, os, logging, sys

from LIBS.classes_V4 import *
from SETTINGS.paths import *
from SETTINGS.settings_test_sampa_regels import *

#some file locations

lidwoorden      = files["lidwoorden"]
voornaamwoorden = files["voornaamwoorden"]
prefixen        = files["prefixen"]
suffixen        = files["suffixen"]
inputf          = files["testlist"]
output          = files["output"]


def split_sampa(ww):
  w=str(ww)
  cons=["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","z"]
  S3vowels=["a:i","o:i","e:u"]
  S2vowels=["Ei","9y","Au","ui","iu","yu","a:","e:","2:","o:","E:","9:","O:"]
  S1vowels=["I","E","A","O","Y","@","i","y","u"]
  WL,CL,VL,skip,error=[],[],[],0,False
  for i in range(len(w)):
    if skip>0:
      skip=skip-1
      continue
    if   w[i] in cons:
      WL.append(w[i])
      CL.append(w[i])
    elif i+2<len(w) and w[i:i+3] in S3vowels: 
      WL.append(w[i:i+3])
      VL.append(w[i:i+3])
      skip=2
    elif i+1<len(w) and w[i:i+2] in S2vowels:
      WL.append(w[i:i+2])
      VL.append(w[i:i+2])
      skip=1
    elif w[i:i+1] in S1vowels:
      WL.append(w[i])
      VL.append(w[i])
  if "".join(WL)!=w: error=True
  return error, WL, CL, VL
  
def remove_accents(input_str):
  import unicodedata, sys
  reload(sys) 
  sys.setdefaultencoding("utf-8")
  nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
  return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def main():
  #the mismatches are stored in result, to be printed after code completion. Nok and Nwr are the counts of successes and failures
  CNok,CNwr,CNchk,result=TotCount(logger,{}),TotCount(logger,{}),TotCount(logger,{}),""
  #add some headers first
  result+= "\n{0} \n\n".format("onjuiste voorspellingen:")
  result+= "{0: <15} \t {1: <15} \t {2: <15}\t {3: <10}\n".format("source","corr. trans.","autom. trans.","warning")
  result+= "{0: <15} \t {1: <15} \t {2: <15}\t {3: <10}\n\n".format("------","------------","-------------","-------")
  
  #N.countword(i)
  #N.printcount(output)
  
  #read the dictionary with left the wordt to be translated, right the correct answer
  D=Dictionary(logger)
  D.add_list_fromfile(voornaamwoorden)
  D.add_list_fromfile(lidwoorden)
  
  
  with open(inputf, "r") as f:
       for line in f:
         words=line.split()
         if len(words)>1:           
           pred=Word(word_from_xml(words[0],None,None,None,None,None), logger, prefixen, suffixen, D, {}).attr["sampa"]
           #if we predict correctly, add one count to successes
           
           testref, reflist, refconsl, refvowl = split_sampa(words[1])
           testpred,predlist,predconsl,predvowl= split_sampa(pred)
           
           if   testref or refconsl!=predconsl: 
             CNchk.countlist(refvowl)
             result+= "{0: <15} \t {1: <15} \t {2: <15}".format(remove_accents(words[0]),remove_accents(words[1]),pred)
             result+= "\t {0: <10}\n".format("CHECK REF")
           elif refvowl == predvowl: 
             CNok.countlist(refvowl)
           else:
             result+= "{0: <15} \t {1: <15} \t {2: <15}\t {3: <10}".format(remove_accents(words[0]),remove_accents(words[1]),pred,"")
             for i in range(len(refvowl)):
               if i<len(predvowl):
                 if refvowl[i] == predvowl[i]:
                   CNok.countlist([refvowl[i]])
                 else: 
                   CNwr.countlist([refvowl[i]])
                   result+= "\t{0: <10}".format(refvowl[i]+" <-- "+predvowl[i])
               else:
                 CNwr.countlist([refvowl[i]])
                 result+= "\t{0: <10}".format(refvowl[i]+" <-- "+"***")
             result+= "\n"
                 
  #synopsis of the test: the scores
  tot=CNok+CNwr+CNchk
  #print tot.count()
  result2= "\n"
  result2+= "correct predictions: {0: <8} ({1: >3}%)\n".format(CNok.count(), int(round(100.0*CNok.count() /(tot.count()))))
  result2+= "wrong predictions:   {0: <8} ({1: >3}%)\n".format(CNwr.count(), int(round(100.0*CNwr.count() /(tot.count()))))
  result2+= "issues with source:  {0: <8} ({1: >3}%)\n".format(CNchk.count(),int(round(100.0*CNchk.count()/(tot.count()))))
  result2+= "total vowels:        {0: <8} ({1: >3}%)\n".format(tot.count(),100)
  result2+= "\ntotal number of occurences of vowels:\n"
  result2+= (tot).printcount(Nohead=True)
  result2+= "\naccuracy per vowel: correct occurence / total occurences\n"
  result2+= (CNok/tot).printcount(Nohead=True)
  result2+= result
  
  #now write all results all at once
  g=open(output, "w")
  g.write(result2)
  g.close()
  

if __name__ == "__main__":
  main()