
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
#  helper functions related to counting and displaying
#  to be converted in object later
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
  