"""
This class defines a "word" that is all attributes gathered about a given word from it's original text.
These attributes include the original string, the corresponding sampa, the position in the sentence, the act and scene it comes from etc
"""

class Word:
  """class used to store a word, with translation and possibly other attributes"""

  def __init__(self, RawWord, preflist, suflist, dictionary, lemmalist, Punctuation=['(', ')', '\\', '"', '\'', '.', ',', ';', ':', '-', '?', '!']):
    """at initialization, the original word is given                         """
    """the word is then cleaned and translated, using the dictionary provided"""
    """a punctuation list is needed to do the cleaning                       """
    import logging
    self.log                = logging.getLogger('sampify')

    self.punctuation        = Punctuation

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

      self.attr["vowel"]      = SampaV(self.attr["sampa"]).vowels

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
          self.attr["sampa"],self.attr["changelog"]=SampaRules().apply(self.attr["sampa"],self.attr["changelog"],self.preflist,self.suflist,self.attr["syllables"],First=self.First,Last=self.Last)
      self.dictionary.add_word_a(self.attr["clean"],self.attr["sampa"])
