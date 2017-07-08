# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 19:35:27 2017
@author: ruben
"""
import logging
class count:
    sampa_double = ["a:", "e:", "2:", "o:", "Ei", "9y", "Au", "E:", "9:", "O:", "A*", "E*", "O*"]
    sampa_single = ["I", "E", "A", "O", "Y", "@", "i", "y", "u", "p", "b", "t", "d", "k", "g", "f", "v", "s", "z",
                         "x", "G", "h", "z", "S", "m", "n", "N", "l", "r", "w", "j"]

    def __init__(self,double=sampa_double, single=sampa_single):
        self.sampa=double+single
        self.count=dict.fromkeys(self.sampa,0)

    def add(self,w):
        wordlist=list(w)
        while len(wordlist)>0:
            if len(wordlist)>1 and wordlist[0]+wordlist[1] in self.sampa_double:
                self.count[wordlist[0]+wordlist[1]]=self.count[wordlist[0]+wordlist[1]]+1
                wordlist=wordlist[2:]
            elif wordlist[0] in self.sampa_single:
                self.count[wordlist[0]]=self.count[wordlist[0]]+1
                wordlist=wordlist[1:]
            else:
                wordlist = wordlist[1:]
                print("warning")

if __name__ == "__main__":
    c=count()
    c.add("EiyXEi")
    print(c.count)


