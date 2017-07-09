# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 19:35:27 2017
@author: ruben
"""
from classes.rules import Rules

class Sampify(Rules):
    def _test_case(self, tvl, tvt, r):
        if type(r) is int:
            if r == 1:
                if tvl != None: return True
            elif r == 0:
                if tvl == None: return True
        elif len(r) == 1:
            if r in ['C', 'V']:
                if r == tvt: return True
            else:
                if r == tvl: return True
        elif len(r) == 3:
            if r[0] in ['C', 'V']:
                if r[2] == '1':
                    if r[0] == tvt: return True
                elif r[2] == '0':
                    if r[0] != tvt: return True
                else:
                    if r[2] == tvl: return True
        return False

    def _test_rule(self, wl, tl, Nsyllab, rule, position, rulenumber):
        all_outcomes = []
        if type(rule['rule']) is int:
            if rule['rule'] == Nsyllab:
                return True
            else:
                return False
        for i in range(len(rule['rule'])):
            if len(wl[position:]) < i + 1:
                all_outcomes.append(self._test_case(None, None, rule['rule'][i]))
            else:
                all_outcomes.append(self._test_case(wl[position:][i], tl[position:][i], rule['rule'][i]))
        if False not in all_outcomes:
            self.log.info("rule {0} is matching".format(rulenumber))
            return True
        self.log.info("rule {0} is not matching".format(rulenumber))
        return False

    def _find_rule(self, wl, tl, Nsyllab, position, rules):
        if position == 0 and wl[0] in rules['P'].keys():
            for i in sorted(rules['P'][wl[position]]['rules'].keys()):
                self.log.info("testing prefix rule {0} of group {1}, letter {2}".format(i, 'P', wl[position]))
                if self._test_rule(wl, tl, Nsyllab, rules['P'][wl[position]]['rules'][i], position, i): return i, rules[
                    'P'][wl[position]]['rules'][i]
        for i in sorted(rules[tl[position]][wl[position]]['rules'].keys()):
            self.log.info("testing rule {0} of group {1}, letter {2}".format(i, tl[position], wl[position]))
            if self._test_rule(wl, tl, Nsyllab, rules[tl[position]][wl[position]]['rules'][i], position, i): return i, \
                                                                                                                    rules[
                                                                                                                        tl[
                                                                                                                            position]][
                                                                                                                        wl[
                                                                                                                            position]][
                                                                                                                        'rules'][
                                                                                                                        i]
        self.log.info("no rule found, default rule is used")
        return 0, rules[tl[position]][wl[position]]['default'][0]

    def _apply_rule(self, log, sampa, position, rule, rulenum):
        srce, dest = list(rule['replaced']), list(rule['replaceby'])
        lensrce, lendest = len(srce), len(dest)
        olog = log[:position] + ['S'] * lendest + log[position + lensrce:]
        osampa = sampa[:position] + dest + sampa[position + lensrce:]
        self.log.info(
            "rule {0} applied to sampa '{1}' on position {2}. Output: '{3}'".format(rulenum, "".join(sampa), position,
                                                                                    "".join(osampa)))
        return olog, osampa

    def _find_apply(self, log, word, syllables, rules):
        for i in range(len(log)):
            if log[i] != 'S':
                self.log.info("searching applicable rule for position {0} of '{1}'".format(i, "".join(word)))
                applicable_rule_n, applicable_rule = self._find_rule(word, log, syllables, i, rules)
                log, word = self._apply_rule(log, word, i, applicable_rule, applicable_rule_n)
                return log, word

    def _num_syll(self, l):
        self.log.info("counting syllables in word")
        if l[0] == 'C':
            vow, lettergrepen = False, 0
        else:
            vow, lettergrepen = True, 1
        for i in range(1, len(l)):
            if l[i] == 'C' and vow == True:  vow = False
            if l[i] == 'V' and vow == False: vow, lettergrepen = True, lettergrepen + 1
        self.log.info("{0} syllables counted".format(lettergrepen))
        return lettergrepen

    def _gen_chlog(self, word):
        word_l, chlog = list(word), []
        for i in word_l:
            if i in self.rules['V'].keys():
                chlog.append('V')
            elif i in self.rules['C'].keys():
                chlog.append('C')
            else:
                chlog.append('S')
                self.log.warn("Unknown letter: '{0}'. Letter will not be translated.".format(i))
        return word_l, chlog

    def clean(self, w):
        import unidecode
        # TO DO: remove punctuation
        self.log.info("removing accents")
        w_noacc=unidecode.unidecode(w.lower())
        return w_noacc
        #for p in self.settings["punctuation"]:
        #    self.CleanWord = self.CleanWord.replace(p, '')

    def translate(self, word):
        self.log.info("starting sampyfication of word '{0}'".format(word))
        word_clean=self.clean(word)
        word_l, chlog = self._gen_chlog(word_clean)
        syllables = self._num_syll(chlog)
        while 'V' in chlog or 'C' in chlog: chlog, word_l = self._find_apply(chlog, word_l, syllables, self.rules)
        self.log.info("word '{0}' successfully sampified: '{1}'".format(word, "".join(word_l)))
        return "".join(word_l)


# standaard woordenlijst
# suffix als 1e doen?
