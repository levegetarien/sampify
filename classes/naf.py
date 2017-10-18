# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 19:35:27 2017
@author: ruben
"""
import logging, unittest

class naf:
    def __init__(self,f):
        import xml.etree.ElementTree as et

        self.log = logging.getLogger('sampify')

        self.tree       = et.parse(f)
        self.root       = self.tree.getroot()
        self.text       = [i for i in self.root.iter() if i.tag == 'text'][0]
        self.terms      = [i for i in self.root.iter() if i.tag == 'terms'][0]
        self.emo        = [i for i in self.root.iter() if i.tag == 'emotions'][0]
        self.log.info("reading words from {0}".format(f))
        self.words      = [word(i)  for i in self.text.iter()  if i.tag == 'wf']
        self.lemmas     = [lemma(i) for i in self.terms]
        self.emolist    = [emotions(i) for i in self.emo if i.tag == 'emotion']

        lemmaByID={i.getTargetID():i for i in self.lemmas}
        self.emolistID  = [i.getID() for i in self.emolist]

        for i in self.words:
            if i.getID() in lemmaByID.keys():
                i.addLemma(lemmaByID[i.getID()])
            for j in range(len(self.emolistID)):
                if i.getLemmaID() in self.emolistID[j]:
                    i.addEmotions(self.emolist[j])
                    break

        # for i in self.words:
        #     if i.isNotPunctuation() and i.getEmotions():
        #         for j in i.getEmotions().getEmotions():
        #             print(i.getWord(), j.getReference())

    def get_wordlist(self, RemovePunctuation=True):
        if RemovePunctuation:
            return [i.getWord() for i in self.words if i.isNotPunctuation()]
        return [i.getWord() for i in self.words]

class emotion:
    def __init__(self,e):
        self.posnegClass={
            'love':'pos',
            'joy':'pos',
            'desire':'pos',
            'hope':'pos',
            'compassion':'pos',
            'happiness':'pos',
            'honor':'pos',
            'loyalty':'pos',
            'wonder':'pos',
            'moved':'pos',
            'aquiescence':'pos',
            'benevolence':'pos',
            'pride':'pos',
            'dedication':'pos',
            'trust':'pos',
            'awe':'pos',
            'relief':'pos',
            'sadness':'neg',
            'fear':'neg',
            'anger':'neg',
            'despair':'neg',
            'vindictiveness':'neg',
            'hatred':'neg',
            'remorse':'neg',
            'worry':'neg',
            'shame':'neg',
            'heavyHeartedness':'neg',
            'disgust':'neg',
            'spitefulness':'neg',
            'annoyance':'neg',
            'envy':'neg',
            'suspicion':'neg',
            'offended':'neg',
            'unhappiness':'neg',
            'dissapointment':'neg',
            'greed':'neg',
            'loss':'neg',
            'other': 'other'
        }
        self.properties={
            'confidence':float(e.attrib['confidence']),
            'reference':e.attrib['reference'].split(':')[1],
            'pos/neg':self.posnegClass[e.attrib['reference'].split(':')[1]]
        }
    def getConfidence(self):
        return self.properties['confidence']
    def getReference(self):
        return self.properties['reference']
    def getPosNeg(self):
        return self.properties['pos/neg']

class emotion_clsuter:
    def __init__(self,c):
        self.posnegClass={
            'sadness':'neg',
            'love':'pos',
            'anger':'neg',
            'fear':'neg',
            'joy':'pos',
            'desire':'pos',
            'despair':'neg',
            'disgust':'neg',
            'posSentiments':'pos',
            'compassion':'pos',
            'prideHonour':'pos',
            'other':'other'
        }
        self.properties={
            'confidence':float(c.attrib['confidence']),
            'reference':c.attrib['reference'],
            'pos/neg':self.posnegClass[c.attrib['reference']]
        }
    def getConfidence(self):
        return self.properties['confidence']
    def getReference(self):
        return self.properties['reference']
    def getPosNeg(self):
        return self.properties['pos/neg']

class emotions:
    def __init__(self,e,th=0.5):
        self.properties={
            'ID':[],
            'threshold':th,
            'emotions':[],
            'clusters':[]
        }

        for i in e.find('span'):
            self.properties['ID'].append(i.attrib['id'])
        for i in e.find('externalReferences'):
            if i.attrib['resource'] == 'heem:clusters':
                self.properties['clusters'].append(emotion_clsuter(i))
            elif i.attrib['resource']=='heem' and i.attrib['reference'].split(':')[0]=='emotionType':
                self.properties['emotions'].append(emotion(i))
    def setThreshold(self,th):
        self.properties['threshold']=th
    def getID(self):
        return self.properties['ID']
    def getEmotions(self):
        return [i for i in self.properties['emotions'] if i.getConfidence()>= self.properties['threshold']]
    def getClusters(self):
        return [i for i in self.properties['clusters'] if i.getConfidence()>= self.properties['threshold']]

class lemma:
    def __init__(self,t):
        self.properties ={
            'ID':t.attrib['id'],
            'lemma':t.attrib['lemma'],
            'pos':t.attrib['pos'],
            'type':t.attrib['type'],
            'targetID':t.find('span').find('target').attrib['id']
        }
    def getTargetID(self):
        return self.properties['targetID']
    def getID(self):
        return self.properties['ID']
    def getLemma(self):
        return self.properties['lemma']
    def getPos(self):
        return self.properties['pos']

class word:
    def __init__(self,w):
        self.properties={
            'word':w.text,
            'ID':w.attrib['id'],
            'length': int(w.attrib['length']),
            'offset': int(w.attrib['offset']),
            'sentence': int(w.attrib['sent']),
            'punctuation':[',', ';', '.', '?', "'", '!' '‘', '&'],
            'lemma':None,
            'lemmaID':None,
            'emotions':None
        }
    def getWord(self):
        return self.properties['word']
    def getID(self):
        return self.properties['ID']
    def isNotPunctuation(self):
        if self.properties['word'] not in self.properties['punctuation']:
            return True
        return False
    def addLemma(self,l):
        self.properties['lemma']=l
        self.properties['lemmaID']=l.getID()
    def addEmotions(self,e):
        self.properties['emotions']=e
    def getEmotions(self):
        return self.properties['emotions']
    def getLemma(self):
        return self.properties['lemma']
    def getLemmaID(self):
        return self.properties['lemmaID']

class TestNaf(unittest.TestCase):
    def setUp(self):
        self.n = naf("/Users/ruben/Projects/Sampify/files/lope001dull01_01.xml")
    def tearDown(self):
        del self.n
    def test_firstword(self):
        self.assertEqual(self.n.get_wordlist()[0], "Stryt", "Incorrect first word")
    def test_isupper(self):
        self.assertEqual(self.n.get_wordlist()[-1], "UYT", "Incorrect last word")

if __name__ == "__main__":
    unittest.main()
