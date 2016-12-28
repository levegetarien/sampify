class SampaV:
  """small class to remember which vowels we have in a word"""

  def __init__(self,w):
    """to initialize, give a 'smart' word, the vowels will be extracted and counted"""
    import logging
    self.vowels,skip={},0
    self.log=logging.getLogger('sampify')

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
    self.somelist=[]
    for i in self.allvowels:
      if self.vowels[i]>0:
        self.somelist.append(i)
    return ' '.join(self.somelist)
