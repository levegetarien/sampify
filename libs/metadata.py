#!/Users/cvr270/Library/Enthought/Canopy_64bit/User/bin/python
import xlrd, sys, logging

class metadata:
  """class containing all metadata sourced from excel"""
  def __init__(self,inp_xls):
    self.log=logging.getLogger('sampify')
    self.wbk  = xlrd.open_workbook(inp_xls)
    self.text = self.parse_sheet(self.wbk,'text')
    self.pers = self.parse_sheet(self.wbk,'pers')
  def parse_sheet(self,workbook,sheetname):
    self.sheet      = workbook.sheet_by_name(sheetname)
    self.headers    = [i.value for i in self.sheet.row(0)]
    self.prop       = []
    for i in range(self.sheet.nrows - 1):
      self.props = {}
      self.row   = [j.value for j in self.sheet.row(i+1)]
      for j in range(len(self.headers)):
        self.props[self.headers[j]]=self.row[j]
      self.prop.append(self.props)
    return self.prop


def main():
  xls_filename = sys.argv[1]
  m=metadata(xls_filename)
  print "Auteur: ", m.text[0]["AUTHOR"]
  for i in range(len(m.pers)):
    print "Personnage " +str(i)+": ", m.pers[i]["NAME"]

if __name__ == "__main__":
  main()
