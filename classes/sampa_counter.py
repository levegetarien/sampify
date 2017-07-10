# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 19:35:27 2017
@author: ruben
"""
import logging, unittest
class count:
    sampa_double = ["a:", "e:", "2:", "o:", "Ei", "9y", "Au", "E:", "9:", "O:", "A*", "E*", "O*"]
    sampa_single = ["I", "E", "A", "O", "Y", "@", "i", "y", "u", "p", "b", "t", "d", "k", "g", "f", "v", "s", "z",
                         "x", "G", "h", "z", "S", "m", "n", "N", "l", "r", "w", "j"]

    def __init__(self,double=sampa_double, single=sampa_single):
        self.log = logging.getLogger('sampify')
        self.sampa=double+single
        self.count=dict.fromkeys(self.sampa,0)

    def add(self,w):
        self.log.info("adding {0} to counter".format(w))
        wordlist=list(w)
        while len(wordlist)>0:
            if len(wordlist)>1 and wordlist[0]+wordlist[1] in self.sampa_double:
                self.count[wordlist[0]+wordlist[1]]=self.count[wordlist[0]+wordlist[1]]+1
                self.log.info("found {0}, adding 1 to total count (was {1})".format(wordlist[0]+wordlist[1], self.count[wordlist[0]+wordlist[1]]-1))
                wordlist=wordlist[2:]
            elif wordlist[0] in self.sampa_single:
                self.count[wordlist[0]]=self.count[wordlist[0]]+1
                self.log.info("found {0}, adding 1 to total count (was {1})".format(wordlist[0], self.count[wordlist[0]]-1))
                wordlist=wordlist[1:]
            else:
                self.log.warning("no corresponding SAMPA found for {0}, removing letter".format(wordlist[0]))
                wordlist = wordlist[1:]

class TestCount(unittest.TestCase):

    def setUp(self):
        self.c = count()
        self.c.add("SEiyEiN")

    def tearDown(self):
        del self.c

    def test_count_single(self):
        self.assertEqual(self.c.count['y'],1, "Incorrect number of 'y' counted")
        self.assertEqual(self.c.count['S'],1, "Incorrect number of 'S' counted")
        self.assertEqual(self.c.count['N'],1, "Incorrect number of 'N' counted")

    def test_count_double(self):
        self.assertEqual(self.c.count['Ei'],2, "Incorrect number of 'Ei' counted")


if __name__ == "__main__":
    unittest.main(verbosity=2)


