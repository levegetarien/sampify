"""
Class to read and process a text (xml or plain text)
The object can translate the words using the word.py class
"""

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