from LIBS.trans_words_class_V3 import *

#########################################################################################
# DEFINITIES VAN CLASSES EN FUNCTIES; ALS DEZE GOED DOORDACHT ZIJN IS DE REST EEN EITJE #
#########################################################################################

class Dictionary:
  """class containing the word equivalency"""

  def __init__(self,log):
    """we do nothing here, except create an empty container"""
    self.sampa={}
    self.log=log

  def add_list_fromfile(self, inf):
    """now here we fill the dictionary, using a file as source      """
    """the source is expected to be plain text, lowercase           """ 
    """ with on every line a word/translation pair, space separated """
    with open(inf,'r') as f:
      for line in f:
        w=line.split()
        if len(w)==2:
          self.sampa[w[0]]=w[1]
          self.log.info("word {0} added to dictionary, corresponding sampa: {1}".format(w[0],w[1]))
        
  def add_word_i(self,W):
    """we also include the option of adding a(n unknown) word interactively"""
    self.sampa[W]=raw_input('please type the sampa translation for \"'+W+'\": ')
    self.log.info("word \"{0}\" added to dictionary, corresponding sampa: \"{1}\"".format(W,self.sampa[W]))
  def add_word_a(self,W,S):
    """we also include the option of adding a(n unknown) word directly"""
    self.sampa[W]=S
    self.log.info("word \"{0}\" added to dictionary, corresponding sampa: \"{1}\"".format(W,self.sampa[W]))

  def save_dict(self,outf):
    """if changes have been made, it is wise to save the enriched dictionary   """
    """the dictionary is saved in the same format as the input file used earlier"""
    with open(outf, "w") as g:
      for i in sorted(self.sampa.keys()):
        g.write("{0: <30} {1: <30}\n".format(i,self.sampa[i]))
    self.log.info("Dictionary saved to file {0}".format(outf))

#########################################################################################    
class Word:
  """class used to store a word, with translation and possibly other attributes"""

  def __init__(self, RawWord, log, preflist, suflist, dictionary, lemmalist, Punctuation=['(', ')', '\\', '"', '\'', '.', ',', ';', ':', '-', '?', '!']):
    """at initialization, the original word is given                         """
    """the word is then cleaned and translated, using the dictionary provided"""
    """a punctuation list is needed to do the cleaning                       """
    
    self.punctuation        = Punctuation
    
    self.log                = log
    self.dictionary         = dictionary
    self.lemmalist          = self.read_lemmafile(lemmalist)
    self.preflist           = self.read_dict(preflist)
    self.suflist            = self.read_dict(suflist)
    
    self.iterations         = 0
    
    self.attr               = {}
    self.attr["input"]      = RawWord.word
    self.attr["position"]   = RawWord.pos
    self.attr["lengte_zin"] = RawWord.len_zin
    self.attr["speaker"]    = RawWord.speaker
    self.attr["act"]        = RawWord.act
    self.attr["scene"]      = RawWord.scene
    self.attr["clean"]      = self.clean(self.attr["input"])    
    if len(self.attr["clean"])==0:
      self.attr["type"]       = None
      self.attr["changelog"]  = []
      self.attr["syllables"]  = 0
      self.attr["sampa"]      = ""    
      self.attr["vowel"]      = SampaV(self.attr["sampa"],self.log).vowels
    else:  
      self.attr["type"]       = self.return_type(self.attr["clean"])
      self.attr["changelog"]  = self.make_clog(self.attr["clean"])
      self.attr["syllables"]  = self.count_syll(self.attr["changelog"])
      self.attr["sampa"]      = self.attr["clean"]
        
      self.sampa()
    
      self.attr["vowel"]      = SampaV(self.attr["sampa"],self.log).vowels
      
  def read_lemmafile(self,f):
    if type(f)==dict: return f
    return xml_lemma(f).lemmas
    
  def return_type(self,w):
    if w in self.lemmalist.keys(): return self.lemmalist[w]#['primary']
    else: return None
          
  def read_dict(self,f,d={}):
    if type(f)==dict: return f
    with open(f, "r") as self.f:
       for self.line in self.f:
         self.words=self.line.split()
         if len(self.words)==2: d[self.words[0]]=self.words[1]
    return d

  def remove_acc(self,w):
    import unicodedata, sys
    reload(sys) 
    sys.setdefaultencoding("utf-8")
    self.nkfd_form = unicodedata.normalize('NFKD', unicode(w))
    self.W_no_accents=u"".join([c for c in self.nkfd_form if not unicodedata.combining(c)])
    self.log.info("Removing accents in word: {0} --> {1}".format(w,self.W_no_accents))
    return self.W_no_accents

  def clean(self, w):
    """self-explanatory: we remove the words from the punctuation list"""
    import unicodedata, sys
    reload(sys) 
    sys.setdefaultencoding("utf-8")
    self.nkfd_form = unicodedata.normalize('NFKD', unicode(w.lower()))
    self.log.info("Removing capitalization in word: {0} --> {1}".format(w,w.lower()))
    self.CleanWord=u"".join([c for c in self.nkfd_form if not unicodedata.combining(c)])
    self.log.info("Removing accents in word:        {0} --> {1}".format(w,self.CleanWord))
    for p in self.punctuation:
      self.CleanWord=self.CleanWord.replace(p, '')
    self.log.info("Removing punctuation in word:    {0} --> {1}".format(w,self.CleanWord))
    return str(self.CleanWord)
    
  def make_clog(self,w):
    self.changelog=[]
    self.klinkers = ["a","e","i","o","u","y"]
    for self.i in w:
      if self.i not in self.klinkers: self.changelog.append(1)    
      else:                           self.changelog.append(0)
    self.log.info("Changelog initialized ({0})".format(self.changelog))
    return self.changelog
    
  def count_syll(self, clog):
    if clog[0] == 1: 
      self.vow,self.lettergrepen=False,0
    else:
      self.vow,self.lettergrepen=True, 1
    for self.i in range(1,len(clog)):
      if clog[self.i]==1 and self.vow==True:
        self.vow=False
      if clog[self.i]==0 and self.vow==False:
        self.vow,self.lettergrepen=True, self.lettergrepen+1
    self.log.info("Syllable count in this word: {0}".format(self.lettergrepen))
    return self.lettergrepen
    
  def sampa(self):
    """translation is done by looking up clean words in a dictionary        """
    """if a word is not present in the dictionary, the translation is asked """
    if len(self.attr["clean"])>0:
      self.log.info("Converting word to sampa: {0}".format(self.attr["clean"]))
      if self.attr["clean"] in self.dictionary.sampa.keys():
        self.log.info("Retrieving Sampa from the dictionary: {0} --> {1}".format(self.attr["clean"],self.dictionary.sampa[self.attr["clean"]]))
        self.attr["sampa"],self.attr["changelog"]=self.dictionary.sampa[self.attr["clean"]],[1 for i in self.attr["sampa"]]
      else:
        self.log.info("No substitutions found, applying rules")
        while 0 in self.attr["changelog"]:# and self.iterations<len(self.attr["clean"]):
          self.First,self.Last=False,False
          self.iterations+=1
          self.log.info("iteration {0}".format(self.iterations))
          if   self.iterations==1:                      self.First=True
          elif self.iterations==self.attr["syllables"]: self.Last= True
          self.attr["sampa"],self.attr["changelog"]=SampaRules(self.log).apply(self.attr["sampa"],self.attr["changelog"],self.preflist,self.suflist,self.attr["syllables"],First=self.First,Last=self.Last)
      self.dictionary.add_word_a(self.attr["clean"],self.attr["sampa"])

#########################################################################################
class Text:
  """class used to store the ensemble of words"""

  def __init__(self,log, preflist, suflist, dictionary,lemmalist):
    """not much is done here"""
    self.log=log
    self.preflist      = self.read_dict(preflist)
    self.suflist       = self.read_dict(suflist)
    self.lemmalist     = self.read_lemma(lemmalist)
    self.fulltext_o    = []
    self.punctuation   = ['(', ')', '\\', '"', '\'', '.', ',', ';', ':', '-', '?', '!']
    self.dictionary    = dictionary

  def add_text_fromfile(self,inf):
    """add a text by pointing at its (plain text) file                                      """
    """note that if this is the second time you call this, the second text will be appended!"""
    self.log.info("reading input file: {0}".format(inf))
    with open(inf,'r') as f:
      allwords=f.read().split()
    allsmartw=[word_from_xml(i,None,None,None,None,None) for i in allwords]
    self.fulltext_o=self.fulltext_o + allsmartw

  def add_text_fromxml(self,inf):
    self.log.info("reading input file: {0}".format(inf))
    text=xml_text(inf)
    textonly=[]
    for i in text.fulltext:
      for j in i.line:
        textonly.append(j)
    self.fulltext_o=self.fulltext_o + textonly
  
  def read_lemma(self,f):
    if type(f)==dict: return f
    self.log.info("reading lemma xml: {0}".format(f))
    return xml_lemma(f).lemmas
  
  def read_dict(self,f,d={}):
    if type(f)==dict: return f
    with open(f, "r") as self.f:
       for self.line in self.f:
         self.words=self.line.split()
         if len(self.words)==2: d[self.words[0]]=self.words[1]
    return d

  def add_punctuation(self,P):
    """if some punctuation is missing in the default list, it can be added"""
    """logically this step is to be performed before translateion!        """
    self.log.info("{0} added to the punctuation list".format(P))
    self.punctuation.append(P)
    
  def translate(self):
    """now all words (string) are magically transformed into smart objects"""
    """the smart objects retain the input, but also clean and translate   """
    """
    self.fulltext_e=[]
    for i in self.fulltext_o:
      self.fulltext_e.append(Word(i,D,self.punctuation))
    """
    self.fulltext_e=[Word(i, self.log, self.preflist, self.suflist,self.dictionary,self.lemmalist,self.punctuation) for i in self.fulltext_o]

  def printword(self,i):
    """just in case we want to see the result!!"""
    print " >> Input: "+self.fulltext_e[i].attr["input"]
    print " >> Clean: "+self.fulltext_e[i].attr["clean"]
    print " >> Sampa: "+self.fulltext_e[i].attr["sampa"]
    if self.fulltext_e[i].attr["vowel"].nvowels >0:
      print " >> Vowel: "+self.fulltext_e[i].attr["vowel"].printused()

#########################################################################################
class SampaV:
  """small class to remember which vowels we have in a word"""
  
  def __init__(self,w,log):
    """to initialize, give a 'smart' word, the vowels will be extracted and counted"""
    self.log,self.vowels,skip=log,{},0
    cons=["b","c","d","f","g","h","j","k","l","m","n","p","q","r","s","t","v","w","x","z"]
    S3vowels=["a:i","o:i","e:u"]
    S2vowels=["Ei","9y","Au","ui","iu","yu","a:","e:","2:","o:","E:","9:","O:"]
    S1vowels=["I","E","A","O","Y","@","i","y","u"]
    self.allvowels=["Ei","9y","Au","a:i","o:i","ui","iu","yu","e:u","I","E","A","O","Y","@","i","y","u","a:","e:","2:","o:","E:","9:","O:"]
    for i in self.allvowels: self.vowels[i]=0
    
    for i in range(len(w)):
      if skip>0:
        skip=skip-1
        continue
      if   w[i] in cons:
        pass
      elif i+2<len(w) and w[i:i+3] in S3vowels: 
        self.vowels[w[i:i+3]]+=1
        skip=2
      elif i+1<len(w) and w[i:i+2] in S2vowels:
        self.vowels[w[i:i+2]]+=1
        skip=1
      elif w[i:i+1] in S1vowels:
        self.vowels[w[i:i+1]]+=1
    
  def printused(self):
    """convert the list of all vowels used to a string"""
    somelist=[]
    for i in self.allvowels:
      if self.vowels[i]>0:
        somelist.append(i)
    return ' '.join(self.somelist)
    
#########################################################################################

class TotCount_Vow:
  """this is a simple counter class"""
  
  def __init__(self,log,vowels={}):
    """we do nothing here, except create an empty container"""
    self.log=log
    self.vowels = vowels
    self.allvowels=["Ei","9y","Au","a:i","o:i","ui","iu","yu","e:u","I","E","A","O","Y","@","i","y","u","a:","e:","2:","o:","E:","9:","O:"]
    if self.vowels=={}:
      for i in self.allvowels: self.vowels[i]=0
    
  def __add__(self,other):
    self.tempvow={}
    for i in self.allvowels:
      self.tempvow[i]=0
      self.tempvow[i]+=(other.vowels[i]+self.vowels[i])
    return TotCount(self.log,self.tempvow)
  def __radd__(self, other):
    if other == 0: return self
    else:          return self.__add__(other)
  def __sub__(self,other):
    self.tempvow={}
    for i in self.allvowels:
      self.tempvow[i]=0
      self.tempvow[i]-=(other.vowels[i]+self.vowels[i])
    return TotCount(self.log,self.tempvow)
  def __div__(self,other):
    self.tempvow={}
    for i in self.allvowels:
      if other.vowels[i] == 0:self.tempvow[i]=0
      elif self.vowels[i] == 0:self.tempvow[i]=0
      else:self.tempvow[i]=round(1.0*self.vowels[i]/other.vowels[i],2)
    return TotCount(self.log,self.tempvow)

  def countword(self,w):
    """this keeps track of how many times vowels of the word are present"""

    for i in self.allvowels:
      self.vowels[i]+=w.attr["vowel"][i]
  
  def countlist(self,l):
    for i in l:
      if i in self.allvowels:
        self.vowels[i]+=1

  def printcount(self,PrintToFile=False,Nohead=False):
    """show the grand total"""
    if PrintToFile:
      g=open(PrintToFile, "w")
      if not Nohead: g.write("####### TOTAL COUNT #######\n")
      for i in sorted(self.vowels.keys()):
        g.write(" >> vowel {0: <4} counted {1}\n".format(i,self.vowels[i]))
      g.close()
    else: 
      A=''
      if not Nohead: A="\n####### TOTAL COUNT #######\n"
      for i in sorted(self.vowels.keys()):
        A+=" >> vowel {0: <4} counted {1}\n".format(i,self.vowels[i])
      return A
  
  def count(self):
    num=0
    for i in self.vowels.keys():
      num+=self.vowels[i]
    return num
    
  def plotfig(self,PrintToFile=False):
      import matplotlib.pyplot as plt
      import numpy as np

      vowels=sorted(self.vowels.keys())
      counts=[self.vowels[i] for i in vowels]

      fig, ax = plt.subplots()
      ax.bar(np.arange(len(counts)), counts,0.5,color='r')
      ax.set_ylabel('count')
      ax.set_title('vowels (sampa)')
      ax.set_xticks(np.arange(len(counts))+0.2)
      ax.set_xticklabels( vowels )
      if PrintToFile: plt.savefig(PrintToFile)
      else: plt.show()
      
#########################################################################################
class xml_lemma:
  def __init__(self,inf):
    self.lemmas=self.parse(inf)
    
  def gettext(self,elem):
    text = elem.text or ""
    for subelem in elem:
        text = text + self.gettext(subelem)
        if subelem.tail:
          text = text + subelem.tail
    return text
    
  def parse(self,inf):
    import sys, subprocess, urllib2, unicodedata
    import xml.etree.ElementTree as ET
    reload(sys) 
    sys.setdefaultencoding("utf-8")
    
    self.lemmalist={}
    
    self.tree = ET.parse(inf)
    self.root = self.tree.getroot()
    
    self.FOUND = [element for element in self.root.iter() if (element.tag == 'w' and 'lemma' in element.attrib and 'type' in element.attrib)]
    for i in self.FOUND:
      self.type={}
      self.type['primary']=i.attrib['type']
      self.sec=[]
      for j in i:
        if j.attrib=={'type':'lexiconMatch'}:
          for k in j:
            if k.attrib == {'type': 'partOfSpeech'}:
              if k.text != None:
                self.sec.append(k.text)
      self.type['secondary']=self.sec
      if i.attrib['lemma'] not in self.lemmalist.keys():
        self.lemmalist[i.attrib['lemma']]=self.type
    return self.lemmalist
    for i in self.lemmalist.keys():
      print "lemma: {0: <15} primary type: {1: <10} secundary type: {2}".format(i, self.lemmalist[i]['primary'],", ".join(self.lemmalist[i]['secondary']))
#########################################################################################
class xml_text:
  def __init__(self,inf):
    self.fulltext=self.xml_parser(inf)
    
  def gettext(self,elem):
    text = elem.text or ""
    for subelem in elem:
      if elem.tag != "note":
        text = text + self.gettext(subelem)
        if subelem.tail:
          text = text + subelem.tail
    return text
    
  def xml_parser(self,xml_filename):
    import sys, subprocess, urllib2, unicodedata
    import xml.etree.ElementTree as ET
    reload(sys) 
    sys.setdefaultencoding("utf-8")
  
    self.sp,       self.lines  = "",[]
    self.newact,   self.Nact   = False,0
    self.newscene, self.Nscene = False,0
    
    self.tree = ET.parse(xml_filename)
    self.root = self.tree.getroot()
    
    self.FOUND = [element for element in self.root.iter() if (element.tag == 'sp' or element.attrib == {'type': 'act'} or element.attrib == {'type': 'scene'})]
    
    for j in self.FOUND:
      if j.tag == 'sp':
        if self.newact==True:
          self.Nact+=1
          self.newact=False
        if self.newscene==True:
          self.Nscene+=1
          self.newscene=False
        for i in j:
          if i.tag == "speaker":
            #for speaker in i:
            #if speaker.tag == "hi":
            self.sp=self.gettext(i)
          if i.tag == "l":# or i.tag=="p":
            self.lines.append(line_from_xml(self.gettext(i),self.sp,self.Nact,self.Nscene))
      elif j.attrib['type']=='act':		self.newact, self.Nscene = True, 0
      elif j.attrib['type']=='scene': self.newscene = True
    return self.lines
      
class line_from_xml:
  def __init__(self,line,speaker,act,scene):
    self.line   = []
    self.speaker= speaker
    self.act    = act
    self.scene  = scene
    
    l=line.split()
    length=len(l)
    for i in range(len(l)):
      self.line.append(word_from_xml(l[i],speaker,act,scene,i+1,length))

class word_from_xml:
  def __init__(self,word,speaker,act,scene,pos,length):
    self.word   = word
    self.speaker= speaker
    self.act    = act
    self.scene  = scene
    self.pos    = pos
    self.len_zin= length
#########################################################################################
def count_vow(m,w):
  allvowels=["Ei","9y","Au","a:i","o:i","ui","iu","yu","e:u","I","E","A","O","Y","@","i","y","u","a:","e:","2:","o:","E:","9:","O:"]
  allvowels=["Ei","9y","Au","a:i","o:i","ui","iu","yu","e:u","I","E","A","O","Y","i","y","u","a:","e:","2:","o:","E:","9:","O:"]
  for i in allvowels:
    if i not in m.keys():
      m[i]=w.attr["vowel"][i]
    else:
      m[i]+=w.attr["vowel"][i]
  return m

def plot_vow(m,PrintToFile=False):
  import matplotlib.pyplot as plt
  import numpy as np
  vowels=sorted(m.keys())
  counts=[m[i] for i in vowels]
  fig, ax = plt.subplots()
  ax.bar(np.arange(len(counts)), counts,0.5,color='r')
  ax.set_ylabel('count')
  ax.set_title('vowels (sampa)')
  ax.set_xticks(np.arange(len(counts))+0.2)
  ax.set_xticklabels( vowels )
  if PrintToFile: plt.savefig(PrintToFile)
  else: plt.show()

def plot_star_vow(m1,m2,m3,PrintToFile=False):
  import matplotlib
  import matplotlib.path as path
  import matplotlib.patches as patches
  import matplotlib.pyplot as plt
  import numpy as np
  v=[i[0] for i in sorted([(i,m1[i]) for i in m1.keys()], key=lambda tup: tup[1])]
  v=sorted(m1.keys())
  v1,v2,v3=[m1[i] for i in v],[m2[i] for i in v],[m3[i] for i in v]
  c1,c2,c3=[100*i/sum(v1) for i in v1],[100*i/sum(v2) for i in v2],[100*i/sum(v3) for i in v3]
  

  properties = v
  matplotlib.rc('axes', facecolor = 'white')

  fig = plt.figure(figsize=(10,8), facecolor='white')
  axes = plt.subplot(111, polar=True)

  t = np.arange(0,2*np.pi,2*np.pi/len(properties))
  plt.xticks(t, [])
  plt.ylim(0,15)
  plt.yticks(np.linspace(0,15,num=4))

  for i in range(len(properties)):
      angle_rad = i/float(len(properties))*2*np.pi
      angle_deg = i/float(len(properties))*360
      ha = "right"
      if angle_rad < np.pi/2 or angle_rad > 3*np.pi/2: ha = "left"
      plt.text(angle_rad, 15.75, properties[i], size=14,
               horizontalalignment=ha, verticalalignment="center")

  values = c1
  t = np.arange(0,2*np.pi,2*np.pi/len(properties))
  couleur='blue'
  points = [(x,y) for x,y in zip(t,values)]
  points.append(points[0])
  points = np.array(points)
  codes = [path.Path.MOVETO,] + \
          [path.Path.LINETO,]*(len(values) -1) + \
          [ path.Path.CLOSEPOLY ]
  _path = path.Path(points, codes)
  _patch = patches.PathPatch(_path, fill=True, color=couleur, linewidth=0, alpha=.3)
  axes.add_patch(_patch)
  _patch = patches.PathPatch(_path, fill=False, linewidth = 2)
  axes.add_patch(_patch)
  plt.scatter(points[:,0],points[:,1], linewidth=2, s=50, color=couleur, edgecolor=couleur, zorder=10)


  values = c2
  t = np.arange(0.01,2*np.pi+0.01,2*np.pi/len(properties))
  couleur='red'
  points = [(x,y) for x,y in zip(t,values)]
  points.append(points[0])
  points = np.array(points)
  codes = [path.Path.MOVETO,] + \
          [path.Path.LINETO,]*(len(values) -1) + \
          [ path.Path.CLOSEPOLY ]
  _path = path.Path(points, codes)
  _patch = patches.PathPatch(_path, fill=True, color=couleur, linewidth=0, alpha=.3)
  axes.add_patch(_patch)
  _patch = patches.PathPatch(_path, fill=False, linewidth = 2)
  axes.add_patch(_patch)
  plt.scatter(points[:,0],points[:,1], linewidth=2, s=50, color=couleur, edgecolor=couleur, zorder=10)

  values = c3
  t = np.arange(0.02,2*np.pi+0.02,2*np.pi/len(properties))
  couleur='green'
  points = [(x,y) for x,y in zip(t,values)]
  points.append(points[0])
  points = np.array(points)
  codes = [path.Path.MOVETO,] + \
          [path.Path.LINETO,]*(len(values) -1) + \
          [ path.Path.CLOSEPOLY ]
  _path = path.Path(points, codes)
  _patch = patches.PathPatch(_path, fill=True, color=couleur, linewidth=0, alpha=.3)
  axes.add_patch(_patch)
  _patch = patches.PathPatch(_path, fill=False, linewidth = 2)
  axes.add_patch(_patch)
  plt.scatter(points[:,0],points[:,1], linewidth=2, s=50, color=couleur, edgecolor=couleur, zorder=10)

  if PrintToFile: plt.savefig(PrintToFile)
  else: plt.show()
  
  
def plot_heatmap(l,PrintToFile=False):

  act_o=1
  sce_o=1
  m={}
  t=[]
  d=[]
  for i in l:  
    act=i.attr["act"]
    sce=i.attr["scene"]
    if act==act_o and sce==sce_o:
      m=count_vow(m,i)
    else:
      d.append(str(act)+':'+str(sce))
      act_o=act
      sce_o=sce
      t.append(m)
      m=count_vow({},i)
    
  labels=["Ei","9y","Au","a:i","o:i","ui","iu","yu","e:u","I","E","A","O","Y","i","y","u","a:","e:","2:","o:","E:","9:","O:"]
  values=[]
  for i in t:
    nn=[]
    for j in labels:
      nn.append(i[j])
    values.append([100.0*k/sum(nn) for k in nn])
  import matplotlib.pyplot as plt
  import numpy as np

  column_labels = d
  row_labels = labels
  data = np.array(values)
  fig, ax = plt.subplots()
  heatmap = ax.pcolor(data, cmap=plt.cm.Blues)
  plt.ylim(0,10)

  # put the major ticks at the middle of each cell
  ax.set_xticks(np.arange(len(labels))+0.5, minor=False)
  ax.set_yticks(np.arange(len(d))+0.5, minor=False)
  ax.set_xlim((0,24))
  ax.set_ylim((0,20))

  # want a more natural, table-like display
  ax.invert_yaxis()
  ax.xaxis.tick_top()

  ax.set_xticklabels(row_labels, minor=False)
  ax.set_yticklabels(column_labels, minor=False)
  ax = plt.gca()
  for t in ax.xaxis.get_major_ticks():
      t.tick1On = False
      t.tick2On = False
  for t in ax.yaxis.get_major_ticks():
      t.tick1On = False
      t.tick2On = False
  if PrintToFile: plt.savefig(PrintToFile)
  else: plt.show()
  