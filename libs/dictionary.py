"""
This class allows to create, read, edit and save dictionaries.
The dictionary stores the equivalence between the original word and the Sampa equivalence.
"""

class Dictionary:
  """class containing the word equivalency"""

  def __init__(self):
    """we do nothing here, except create an empty container"""
    import logging
    self.sampa={}
    self.log=logging.getLogger('sampify')

  def add_list_fromfile(self, inf):
    """now here we fill the dictionary, using a file as source      """
    """the source is expected to be plain text, lowercase           """
    """ with on every line a word/translation pair, space separated """
    with open(inf,'r') as f:
      for line in f:
        w=line.split()
        if len(w)==2:
          self.sampa[w[0]]=w[1]
          self.log.info("word {0} added to dictionary, corresponding sampa: {1}".format(w[0],w[1]))

  def add_word_i(self,W):
    """we also include the option of adding a(n unknown) word interactively"""
    self.sampa[W]=raw_input('please type the sampa translation for \"'+W+'\": ')
    self.log.info("word \"{0}\" added to dictionary, corresponding sampa: \"{1}\"".format(W,self.sampa[W]))

  def add_word_a(self,W,S):
    """we also include the option of adding a(n unknown) word directly"""
    self.sampa[W]=S
    self.log.info("word \"{0}\" added to dictionary, corresponding sampa: \"{1}\"".format(W,self.sampa[W]))

  def save_dict(self,outf):
    """if changes have been made, it is wise to save the enriched dictionary   """
    """the dictionary is saved in the same format as the input file used earlier"""
    with open(outf, "w") as g:
      for i in sorted(self.sampa.keys()):
        g.write("{0: <30} {1: <30}\n".format(i,self.sampa[i]))
    self.log.info("Dictionary saved to file {0}".format(outf))
