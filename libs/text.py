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