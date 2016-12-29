"""
This class defines a "word" that is all attributes gathered about a given word from it's original text.
These attributes include the original string, the corresponding sampa, the position in the sentence, the act and scene it comes from etc
"""

class Word:
  """class used to store a word, with translation and possibly other attributes"""

  def __init__(self, prefixes, suffixes, dictionary, lemmas, properties, emotions, sampadef, maxiter=3, punctuation=['(', ')', '\\', '"', '\'', '.', ',', ';', ':', '-', '?', '!']):
    """at initialization, the original word is given                         """
    """the word is then cleaned and translated, using the dictionary provided"""
    """a punctuation list is needed to do the cleaning                       """
    import logging
    self.log                = logging.getLogger('sampify')

    self.settings={
        "punctuation":punctuation,
        "dictionary" :dictionary,
        "prefixes"   :prefixes,
        "suffixes"   :suffixes,
        "lemmas"     :lemmas,
        "properties" :properties,
        "emotions"   :emotions,
        "sampadef"   :sampadef}

    self.admin={
        "maxitereations" :maxiter,
        "syllables"      :0}

    self.attributes={
        "original_word" :None,
        "position"      :None,
        "length_sentece":None,
        "speaker"       :None,
        "act"           :None,
        "scene"         :None,
        "clean_word"    :None,
        "word_type"     :None,
        "sampa"         :None,
        "vowel_count"   :None,
        "cons_count"    :None,
        "emotions"      :None}

  def add_word(self,word,position,length_sentece,speaker,act,scene):
      self.attributes["original_word"]  = word
      self.attributes["position"]       = positions
      self.attributes["length_sentece"] = length_sentece
      self.attributes["speaker"]        = speaker
      self.attributes["act"]            = scene
      self.attributes["scene"]          = act

      #clean
      self.attributes["clean_word"]     = self.clean(self.attributes["original_word"])

      #convert to sampa
        #count wowels
        #count consonnants

      #connect with emotions

      #extract type
      self.attributes["word_type"]      = self.return_type(self.attributes["clean_word"])

  def clean(self, w):
    """self-explanatory: we remove the words from the punctuation list"""
    import unicodedata, sys
    reload(sys)
    sys.setdefaultencoding("utf-8")
    self.nkfd_form = unicodedata.normalize('NFKD', unicode(w.lower()))
    self.log.info("Removing capitalization in word: {0} --> {1}".format(w,w.lower()))
    self.CleanWord=u"".join([c for c in self.nkfd_form if not unicodedata.combining(c)])
    self.log.info("Removing accents in word:        {0} --> {1}".format(w,self.CleanWord))
    for p in self.settings["punctuation"]:
      self.CleanWord=self.CleanWord.replace(p, '')
    self.log.info("Removing punctuation in word:    {0} --> {1}".format(w,self.CleanWord))
    return str(self.CleanWord)

  def return_type(self,w):
    if w in self.lemmalist.keys(): return self.lemmalist[w]#['primary']
    else: return None
