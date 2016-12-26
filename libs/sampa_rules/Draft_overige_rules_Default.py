class DefaultConsonantRules (SampaRules):
  pass

  def double_rule_consonants(self,nlds,chlog,startpos,w):
    rule,smpa=0,nlds
    dubbelconsonantMap = {  "bb":(1,"b"),   "ch":(2,"x"),   "dd":(3,"d"),   "ff":(4,"f")  
                        ,   "gg":(5,"G"),   "gh":(6,"g"),   "hh":(7,"h"),   "jj":(8,"j")
                        ,   "kk":(9,"k"),   "ll":(10,"l"),  "mm":(11,"m"),  "nn":(12,"n")
                        ,   "ng":(13,"N"),  "pp":(14,"p"),  "qq":(15,"k"),  "rr":(16,"r")
                        ,   "ss":(17,"s"),  "sz":(18,"s"),  "sj":(19,"S"),  "sh":(20,"S")
                        ,   "tt":(21,"t"),  "vv":(22,"v"),  "ww":(23,"w"),  "xx":(24,"s")
                        ,   "zz":(25,"z"),  "zj":(26,"Z")}
                        
# opletten bij vv en ww combinaties als er een u bij voorkomt, verandert dat de zaak, WELLICHT NOG AANPASSEN IN U-REGEL? 

    if nlds in dubbelconsonantMap.keys():
      rule,smpa=dubbelconsonantMap[nlds][0],dubbelconsonantMap[nlds][1]
    return rule,smpa

# Hieronder een def voor triple consonants. Sch gaat zonder die triples ook wel goed, maar in twee van de varianten A t/m D moet sch gewijzigd worden in sampa sk, dus het leek me handiger de triple variant ook aan te leggen als def. 

  def triple_rule_consonants(self,nlds,chlog,startpos,w):
    rule,smpa=0,nlds
    tripleconsonantMap = {  "sch":(1,"sx")}
    if nlds in tripleconsonantMap.keys():
      rule,smpa=tripleconsonantMap[nlds][0],tripleconsonantMap[nlds][1]
    return rule,smpa 
    
# Hieronder de rules voor individuele medeklinkers:

  def b_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"b"
    if startpos==len(w)-1: #laatste letter woord
      rule,smpa=1,"p"
    elif startpos==len(w)-2 and w[startpos+1] in ["t", "d"]:  
      rule,smpa=2,"p" 
    return rule,smpa
  
  def c_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"k"
    if len(chlog)>startpos+1 and w[startpos+1] in ["e", "i"]:
      rule,smpa=1,"s"
    elif len(chlog)>startpos+1 and w[startpos+1]=="c":
      rule,smpa=2,"k"
    return rule,smpa
         
  def d_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"d"
    if startpos==len(w)-1: #laatste letter woord
      rule,smpa=1,"t"
    elif startpos==len(w)-2: and w[startpos+1] in [consonants] #voorlaatste letter woord, gevolgd door medeklinker. VRAAG:  Indien gevolgd door t, zou er nu tt ontstaan. Wordt die dan automatisch als dubbelconsonant behaldeld? dus tt = sampa t 
      rule,smpa=2,"t"
    return rule,smpa
 
  def f_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"f"
    return rule,smpa

  def g_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"G"
    return rule,smpa
 
  def h_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"h"
    return rule,smpa
   
  def j_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"j"
    return rule,smpa

  def k_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"k"
    return rule,smpa

  def l_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"l"
    return rule,smpa
    
  def m_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"m"
    return rule,smpa
    
  def n_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"n"
    return rule,smpa
    
  def p_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"p"
    return rule,smpa
    
  def q_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"k"
    if len(chlog)>startpos+1 and w[startpos+1]=="u":
      rule,smpa=1,"kw"
    return rule,smpa
    
  def r_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"r"
    return rule,smpa
    
  def s_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"s"
    return rule,smpa

  def t_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"t"
    return rule,smpa    

  def v_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"v"
    return rule,smpa
    
  def w_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"w"
    return rule,smpa

  def x_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"ks"
    return rule,smpa
# VRAAG: kan dit zonder problemen? 1 letter /x/ moet vertaald naar 2 Sampa letters: ks
    
  def z_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"z"
    return rule,smpa
