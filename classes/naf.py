# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 19:35:27 2017
@author: ruben
"""
import logging, unittest
class naf:
    def __init__(self,f):
        self.log = logging.getLogger('sampify')
        import xml.etree.ElementTree as et

        self.tree  = et.parse(f)
        self.root  = self.tree.getroot()
        self.text  = [i for i in self.root.iter() if i.tag == 'text'][0]
        self.log.info("reading words from {0}".format(f))
        self.words = [i for i in self.text.iter() if i.tag == 'wf']

        #for i in self.words: print(i.attrib['id'])

    def get_wordlist(self):
        return [i.text for i in self.words]

    def get_wordlist_nopunct(self):
        return [i.text for i in self.words if i.text not in [',', ';', '.', '?', "'", '!' '‘', '&']]


class TestNaf(unittest.TestCase):

    def setUp(self):
        self.n = naf("/Users/cvr270/PycharmProjects/Sampify/files/in/naf_alew001besl01_01.xml")

    def tearDown(self):
        del self.n

    def test_firstword(self):
        self.assertEqual(self.n.get_wordlist_nopunct()[0], "Beslikte", "Incorrect first word")

    def test_isupper(self):
        self.assertEqual(self.n.get_wordlist_nopunct()[-1], "Einde", "Incorrect last word")

if __name__ == "__main__":
    unittest.main()
