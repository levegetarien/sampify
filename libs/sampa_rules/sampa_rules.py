class SampaRules:
  def __init__(self):
    import logging
    self.log=logging.getLogger('sampify')

  def update_word(self, w, cl, startpos, bron, sampa,rule):
    if   rule==100:
      self.log.info("  prefix found, ('{0}')".format(bron))
    elif rule==101:
      self.log.info("  suffix found, ('{0}')".format(bron))
    elif len(bron)==1:
      if rule == 0: self.log.warn("  single vowel '{0}', but no rule (word '{1}' at position {2})".format(bron,w,startpos+1))
      self.log.info("  single vowel, rule {1}.{0}  ('{1}' replaced by '{2}')".format(rule,bron,sampa))
    elif len(bron)==2:
      if rule == 0: self.log.warn("  double vowel '{0}', but no rule (word '{1}' at position {2})".format(bron,w,startpos+1))
      self.log.info("  double vowel, rule {0}  ('{1}' replaced by '{2}')".format(rule,bron,sampa))
    elif len(bron)==3:
      if rule == 0: self.log.warn("  triple vowel '{0}', but no rule (word '{1}' at position {2})".format(bron,w,startpos+1))
      self.log.info("  triple vowel, rule {0}  ('{1}' replaced by '{2}')".format(rule,bron,sampa))

    oldw=w
    w=w[:startpos]+sampa+w[startpos+len(bron):]
    cl[startpos:startpos+len(bron)]=[1]*len(sampa)
    self.log.info("    on position {0}: replacing \"{1}\" by \"{2}\"".format(startpos+1,bron,sampa))
    self.log.info("    {0: <15} -->      {1: <15}".format(oldw,w))
    return w, cl

  def apply(self,w, chlog, prefix, suffix, N,First=False,Last=False):

    self.startpos=chlog.index(0)
    self.thischar=w[self.startpos]
    self.dubbelklink,self.tripleklink=False,False

    if len(chlog)>self.startpos+1 and chlog[self.startpos+1]== 0:
      self.dubbelklink=True
      self.Nextchar=w[self.startpos+1]
      if len(chlog)>self.startpos+2 and chlog[self.startpos+2]==0:
        self.tripleklink=True
        self.Nnxtchar=w[self.startpos+2]
        if len(chlog)>self.startpos+3 and chlog[self.startpos+3]==0:
          self.log.error("four sequential vowels detected in word '{0}' at posiotion '{1}', no rule to handle this!".format(w,self.startpos+1))

    #driedubbele letters
    if self.tripleklink==True:
      self.nlds = self.thischar+self.Nextchar+self.Nnxtchar
      self.rule,self.smpa= self.triple_rule(self.nlds,chlog,self.startpos,w)
      w,chlog=self.update_word(w,chlog,self.startpos,self.nlds,self.smpa,self.rule)

    #dubbele letters
    elif self.dubbelklink==True:
      self.nlds = self.thischar+self.Nextchar
      self.rule,self.smpa= self.double_rule(self.nlds,chlog,self.startpos,w)
      w,chlog=self.update_word(w,chlog,self.startpos,self.nlds,self.smpa,self.rule)

    #prefix en suffixen
    if First:
      for self.i in prefix.keys():
         if w[:len(self.i)]==self.i and 0 in chlog[:len(self.i)]:
          w,chlog = self.update_word(w,chlog,0,self.i,prefix[self.i],100)
          return w, chlog

    if Last:
      for self.i in suffix.keys():
        if w[-len(self.i):]==self.i:
          w,chlog = self.update_word(w,chlog,len(w)-len(self.i),self.i,suffix[self.i],101)
          return w, chlog

    #enkele klinkers
    if self.dubbelklink==False:
      functionmap={"a":self.a_rule, "o":self.o_rule, "u":self.u_rule, "i":self.i_rule, "e":self.e_rule, "y":self.y_rule}
      self.nlds,rule=self.thischar,functionmap[self.thischar]
      self.rule,self.smpa=rule(self.startpos,w,chlog,N)
      w,chlog=self.update_word(w,chlog,self.startpos,self.nlds,self.smpa,self.rule)

    return w, chlog

  def triple_rule(self,nlds,chlog,startpos,w):
    rule,smpa=0,nlds
    tripleklinkMap = { "aai":(1,"a:i"), "aaj":(2,"a:i"), "ooi":(3,"o:i") , "oei":(4,"ui"), "ieu":(5,"i2:"), "eeu":(6,"e:u"), "eau":(7,"o:")}
    if nlds == "ieu" and len(chlog)>startpos+3 and w[startpos+3] == "w":
      rule,smpa=8,"iu"
    elif nlds in tripleklinkMap.keys():
      rule,smpa=tripleklinkMap[nlds][0],tripleklinkMap[nlds][1]
    return rule,smpa

  def double_rule(self,nlds,chlog,startpos,w):
    rule,smpa=0,nlds
    dubbelklinkMap = { "au":(1,"Au"), "eu":(2,"2:"),   "ou":(3,"Au") ,  "ui":(4,"9y"),   "ei":(5,"Ei"),  "oe":(6,"u"),  "ue":(7,"y")
                     , "ie":(8,"i"),  "aa":(9,"a:"),   "ae":(10,"a:"),  "ee":(11,"e:"),  "oo":(12,"o:"), "uu":(13,"y"), "ai":(14,"E:")
                     , "yy":(15,"y"), "io":(16,"io:"), "ia":(17,"ia:"), "ya":(18,"ia:"), "ey":(19,"Ei"), "uy":(20,"9y")}
    if nlds in dubbelklinkMap.keys():
      rule,smpa=dubbelklinkMap[nlds][0],dubbelklinkMap[nlds][1]
    return rule,smpa

  def a_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"A"
    if len(chlog)>startpos+2 and  w[startpos+1:startpos+3] in ["ng","ch"]:#ch en ng regel
      rule,smpa=1,"A"
    elif len(chlog)>startpos+2 and chlog[startpos+2]==1:#gevolgd door 2 medeklinkers
      rule,smpa=2,"A"
    elif startpos==len(w)-1:#laatste letter van woord
      rule,smpa=3,"a:"
    elif N==1:#maar een enkele lettergreep
      rule,smpa=4,"A"
    elif len(chlog)>startpos+2 and chlog[startpos+2]==0:#gevolgd door medeklinker en dan klinker
      rule,smpa=5,"a:"
    elif len(chlog)==startpos+2:#laatste klinker van het woord, gevolgd door 1 medeklinker
      rule,smpa=6,"A"
    elif len(chlog)==startpos+3 and chlog[startpos+2]==1:#laatste klinker van het woord, gevolgd door 2 medeklinkers  #!! zie regel 2
      rule,smpa=7,"A"
    return rule,smpa

  def o_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"O"
    if len(chlog)>startpos+2 and  w[startpos+1:startpos+3] in ["ng","ch"]:#ch en ng regel
      rule,smpa=1,"O"
    elif len(chlog)>startpos+2 and chlog[startpos+2]==1:#gevolgd door 2 medeklinkers
      rule,smpa=2,"O"
    elif startpos==len(w)-1:#laatste letter van woord
      rule,smpa=3,"o:"
    elif N==1:#maar een enkele lettergreep
      rule,smpa=4,"O"
    elif len(chlog)>startpos+2 and chlog[startpos+2]==0:#gevolgd door medeklinker en dan klinker
      rule,smpa=5,"o:"
    elif len(chlog)==startpos+2:#laatste klinker van het woord, gevolgd door 1 medeklinker
      rule,smpa=6,"O"
    elif len(chlog)==startpos+3 and chlog[startpos+2]==1:#laatste klinker van het woord, gevolgd door 2 medeklinkers  #!! zie regel 2
      rule,smpa=7,"O"
    return rule,smpa

  def u_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"Y"
    if len(chlog)>startpos+2 and  w[startpos+1:startpos+3] in ["ng","ch"]:#ch en ng regel
      rule,smpa=1,"Y"
    elif len(chlog)>startpos+1 and w[startpos+1]=="w":#gevolgd door een w
      rule,smpa=2,"yu"
    elif len(chlog)>startpos+2 and chlog[startpos+2]==1:#gevolgd door 2 medeklinkers
      rule,smpa=3,"Y"
    elif startpos==len(w)-1:#laatste letter van woord
      rule,smpa=4,"y"
    elif N==1:#maar een enkele lettergreep
      rule,smpa=5,"Y"
    elif len(chlog)>startpos+2 and chlog[startpos+2]==0:#gevolgd door medeklinker en dan klinker
      rule,smpa=6,"y"
    elif len(chlog)==startpos+2:#laatste klinker van het woord, gevolgd door 1 medeklinker
      rule,smpa=7,"Y"
    elif len(chlog)==startpos+3 and chlog[startpos+2]==1:#laatste klinker van het woord, gevolgd door 2 medeklinkers  #!! zie regel 3
      rule,smpa=8,"Y"
    return rule,smpa

  def i_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"I"
    if len(chlog)>startpos+2 and  w[startpos+1:startpos+3] in ["ng","ch"]:#ch en ng regel
      rule,smpa=1,"I"
    elif w[startpos+1:startpos+3]=="jk":#-ijk
      rule,smpa=2,"@"
    elif len(chlog)>startpos+1 and w[startpos+1]=="j":#ij
      rule,smpa=3,"Ei"
    elif len(chlog)>startpos+2 and chlog[startpos+2]==1:#gevolgd door 2 medeklinkers
      rule,smpa=4,"I"
    elif startpos==len(w)-1:#laatste letter van woord
      rule,smpa=5,"i"
    elif N==1:#maar een enkele lettergreep
      rule,smpa=6,"I"
    elif len(chlog)>startpos+2 and chlog[startpos+2]==0:#gevolgd door medeklinker en dan klinker
      rule,smpa=7,"i"
    elif len(chlog)>startpos+1 and w[startpos+1]=='g':#-ig
      rule,smpa=8,"@"
    elif len(chlog)==startpos+2:#laatste klinker van het woord, gevolgd door 1 medeklinker
      rule,smpa=9,"I"
    elif len(chlog)==startpos+3 and chlog[startpos+2]==1:#laatste klinker van het woord, gevolgd door 2 medeklinkers  #!! zie regel 4
      rule,smpa=10,"I"
    return rule,smpa

  def e_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"@"
    if startpos==len(w)-1:#laatste letter van een woord
      rule,smpa=1,"@"
    elif len(chlog)>startpos+1 and  w[startpos+1:startpos+3] in ["ng","ch"]:#ch en ng regel
      rule,smpa=2,"E"
    elif N==1:#maar een enkele lettergreep
      rule,smpa=3,"E"
    elif startpos==0 and len(chlog)>startpos+2 and chlog[startpos+2]==0:#eerste letter, gevolgd door medeklinker en dan klinker
      rule,smpa=4,"e:"
    elif len(chlog)>startpos+2 and chlog[startpos+2]==1:#laatste klinker van het woord, gevolgd door 2 medeklinkers
      rule,smpa=5,"E"
    elif len(chlog)>startpos+3 and w[startpos+1:startpos+4] == "lyk":#-elyk
      rule,smpa=6,"@"
    elif len(chlog)>startpos+4 and w[startpos+1:startpos+5] == "lijk":#-elijk
      rule,smpa=7,"@"
    elif len(chlog)==startpos+2:#laatste klinker van het woord, gevolgd door 1 medeklinker
      rule,smpa=8,"@"
    return rule,smpa

  def y_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"Ei"
    return rule,smpa
