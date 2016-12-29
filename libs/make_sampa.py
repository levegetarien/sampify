class Sampa:
    def __init__(self,dictionary,prefixes,suffixes,maxiter):
        import logging
        self.log  = logging.getLogger('sampify')

        self.settings={
            "dictionary":dictionary,
            "prefixes"  :prefixes,
            "suffixes"  :suffixes,
            "maxiter"   :maxiter,
            "klinkers"  :["a","e","i","o","u","y"]}

    def make_clog(self,w):
        self.changelog=[]
        for self.i in w:
              if self.i not in self.settings["klinkers"]: self.changelog.append(1)
              else:                                       self.changelog.append(2)
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
            if clog[self.i]==2 and self.vow==False:
                self.vow,self.lettergrepen=True, self.lettergrepen+1
        self.log.info("Syllable count in this word: {0}".format(self.lettergrepen))
        return self.lettergrepen

    def convert(self,w):
        word={
            "input"     :w,
            "changelog" :self.make_clog(w),
            "progress"  :"B",
            "syllables" :self.count_syll(word["changelog"])
            "output"    :""}

        if len(w)>0:
            if w in self.settings["dictionary"].sampa.keys():
                self.log.info("Retrieving Sampa from the dictionary: {0} --> {1}".format(w,self.settings["dictionary"].sampa[w]))
                self.word["output"],self.word["changelog"]=self.settings["dictionary"].sampa[w],[1 for i in self.word["changelog"]]
            else:

        #chek if portion of word not in suflist or preflist
        #if changelog contains at least a 1, convert vowels
        #if changelog contains no 1 but at least one 2, convert consonnants
        #count consonnants and vowels
        #retun the translated word, iterations, syllable count and consonnants and vowel count


"""
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
  else: return w
 """
