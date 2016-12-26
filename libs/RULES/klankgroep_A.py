class klankgroepA(SampaRules):
  pass
  

# KLANKGROEP A (1650+, Holland)
# Afwijkingen ten opzichte van Default

  def ou_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"Au"
    if len(chlog)>startpos+1 and w[startpos+1] in ["b", "f", "g", "k", "m", "p", "v", "w"]:
      rule,smpa=1,"u"
    return rule,smpa

  def ij_rule(self,startpos,w,chlog,N):
    rule,smpa=0,"Ei"
    if len(chlog)>startpos+1 and w[startpos+1]=="r":
      rule,smpa=1,"i"  
    return rule,smpa      

# VRAAG: hoe verwerken we de variaties in spelling van ij (te weten: ii, y, ej, ei, ey)? Die moeten volgens dezelfde regel als ij_rule behandeld worden in groep A

  def uu_rule(self,startpos,w,chlog,N):
     rule,smpa=0,"9y"
     if len(chlog)>startpos+1 and w[startpos+1]=="r":
       rule,smpa=1,"y"
     return rule,smpa

# VRAAG: hoe verwerken we de variatie in spelling van uu (te weten: ue)?




# lange ij / ii / y		Ei 	tenzij gevolgd door / r / dan vertalen als SAMPA = i
#variaties van spellingen lange ij zijn ook ej / ei / ey

#lange u 			9y	tenzij gevolgd door / r /. Dus: ue / ui = SAMPA 9y, maar gevolgd door / r / vertalen als SAMPA = y



#ou 				Au	tenzij gevolgd door g / k / p / b / v / f / w / m / —> in die gevallen vertalen als SAMPA = u

#/aa/ klank veel als aa gespeld, dus volgt gewoon schrift, hoeft niet aangepast in rules

#ae 				a:
#ee				e:

#sch midden woord	= sampa s

#geen sjwa (ontstond loop 18e eeuw)