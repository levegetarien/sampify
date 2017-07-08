# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 19:35:27 2017
@author: ruben
"""
import logging
class naf:
    def __init__(self,f):
        import xml.etree.ElementTree as et

        self.tree  = et.parse(f)
        self.root  = self.tree.getroot()
        self.text  = [i for i in self.root.iter() if i.tag == 'text'][0]
        self.words = [i for i in self.text.iter() if i.tag == 'wf']

        #for i in self.words:
            #print(i.attrib['id'])

    def get_wordlist(self):
        return [i.text for i in self.words]

    def get_wordlist_nopunct(self):
        return [i.text for i in self.words if i.text not in [',', ';', '.', '?', "'", '!' '‘', '&']]



            #print(len(self.words))

        # self.FOUND = [element for element in self.root.iter() if
        #               (element.tag == 'sp' or element.attrib == {'type': 'act'} or element.attrib == {'type': 'scene'})]


if __name__ == "__main__":
    n=naf("/Users/cvr270/PycharmProjects/Sampify/files/in/naf_alew001besl01_01.xml")
    print(n.get_wordlist_nopunct())
