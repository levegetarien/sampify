# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 19:35:27 2017
@author: ruben
"""
import logging
class Rules:
    def __init__(self, f=None):
        self.log = logging.getLogger('sampify')
        self.rules = {'C': {}, 'V': {}, 'P': {}}
        if f != None: self.add_rules(fromfile=f)

    def add_rules(self, fromfile=False, fromline=False):
        if fromline:
            rules = self._read_line_rule()
        if fromfile:
            if fromfile[-4:] == '.csv':
                rules = self._read_csv(fromfile)
            elif fromfile[-5:] == '.json':
                rules = self._read_json(fromfile)
            elif fromfile[-5:] == '.xlsx':
                self._xlsx_to_csv(fromfile, fromfile[:-5] + "_imported_from_xlsx.csv")
                rules = self._read_csv(fromfile[:-5] + "_imported_from_xlsx.csv")
        if fromfile or fromline:
            self._add_rules(rules)

    def _read_line_rule(self):
        lettyp = str(self.inp('C, V or P? '))
        letter = str(self.inp('first letter? '))
        rultyp = str(self.inp('rules or default? [r/d] '))
        number = int(self.inp('rule number? '))
        descrn = str(self.inp('description? '))
        rulstx = eval(self.inp('rule syntax? '))
        rplced = str(self.inp('letters to be replaced? '))
        rplcby = str(self.inp('replace by? '))
        if lettyp in ['C', 'V', 'P'] and rultyp in ["default", "rules", "r", "d"]:
            if rultyp == 'r':
                rultyp = "rules"
            elif rultyp == 'd':
                rultyp = "default"
            return {lettyp: {letter: {
                rultyp: {number: {"description": descrn, "rule": rulstx, "replaced": rplced, "replaceby": rplcby}}}}}
        else:
            print("wrong input, nothing added")
            return {}

    def inp(self, s):
        return input(s)

    def _add_rules(self, rules):
        self.log.warning(
            "combining rules can negatively affect the order of rules. Always check the combination of rules manually")
        for i in rules.keys():
            for j in rules[i].keys():
                if j not in self.rules[i].keys():  # case where a letter was not in the rule set yet
                    self.rules[i][j] = {'default': {}, 'rules': {}}
                    if 'default' in rules[i][j].keys():
                        for k in rules[i][j]['default'].keys():
                            self.log.info("checking rule {0}:{1}:default:{2} before adding".format(i, j, k))
                            self._check_rule_syntax(rules[i][j]['default'][k])
                        self.rules[i][j]['default'] = rules[i][j]['default']
                        self.log.info("all {0}:{1}:default rules added".format(i, j))
                    else:
                        self.log.warning("{0}:{1} might not have a default".format(i, j))
                    if 'rules' in rules[i][j].keys():
                        for k in rules[i][j]['rules'].keys():
                            self.log.info("checking rule {0}:{1}:rules:{2} before adding".format(i, j, k))
                            self._check_rule_syntax(rules[i][j]['rules'][k])
                        self.rules[i][j]['rules'] = rules[i][j]['rules']
                        self.log.info("all {0}:{1}:rules rules added".format(i, j))
                else:
                    if 'default' in rules[i][j].keys() and len(self.rules[i][j]['default'].keys()) > 0:
                        self.log.warning(
                            "default rule already present for {0}:{1}, while trying to add one. There might be multiple defaults now".format(
                                i, j))
                    for k in rules[i][j].keys():
                        for l in rules[i][j][k].keys():
                            if l not in self.rules[i][j][k].keys():
                                self.log.info("checking rule {0}:{1}:{2}:{3} before adding".format(i, j, k, l))
                                self._check_rule_syntax(rules[i][j][k][l])
                                self.rules[i][j][k][l] = rules[i][j][k][l]
                                self.log.info("rule {3} added to {0}:{1}:{2}".format(i, j, k, l))
                            else:
                                self.log.warning(
                                    "attempting to overwrite a rule, new rule was ignored. (rule {0}:{1}:{2}:{3})".format(
                                        i, j, k, l))

    def _check_rule_syntax(self, l):
        if type(l["rule"]) == int:
            if l["rule"] < 1:
                self.log.warning("A rule has a too small required number of syllables: {0}".format(l["rule"]))
            elif l["rule"] > 10:
                self.log.warning("A rule has a very high required number of syllables: {0}".format(l["rule"]))
        elif type(l["rule"]) == list:
            for m in l["rule"]:
                if type(m) == int:
                    if m not in [0, 1]:
                        self.log.warning(
                            "the syntax within a rule is badly formed, presence/absence of a character should be expressed with 1/0: {0}".format(
                                l["rule"]))
                else:
                    if len(m) not in [1, 3]:
                        self.log.warning(
                            "the syntax within a rule is badly formed, it should be expressed in 1 or 3 characters: {0}".format(
                                l["rule"]))
                    if len(m) == 3 and m[1] != '=':
                        self.log.warning(
                            "the syntax within a rule is badly formed, it should be united by an = sign: {0}".format(
                                l["rule"]))
                    if len(m) == 3 and m[0] not in ["V", "C"]:
                        self.log.warning(
                            "the syntax within a rule is badly formed, the left side of the equation should be C or V: {0}".format(
                                l["rule"]))

    def _read_json(self, f):
        import json
        with open(f) as data_file:
            self.log.info("json rule file {0} successfully parsed".format(f))
            return json.load(data_file)

    def _write_json(self, f):
        import json
        with open(f, 'w') as outfile:
            json.dump(self.rules, outfile, indent=4, sort_keys=True, separators=(',', ':'))
            self.log.info("json rule file {0} successfully written".format(f))

    def _read_csv(self, f):
        with open(f) as data_file:
            content = [x.strip() for x in data_file.readlines()]
            rules, headers = {}, content[0].split(';')
            for i in content[1:]:
                elements = i.split(';')
                if elements[0] not in rules.keys():
                    rules[elements[0]] = {}
                if elements[1] not in rules[elements[0]].keys():
                    rules[elements[0]][
                        elements[1]] = {}
                if elements[2] not in rules[elements[0]][elements[1]].keys():
                    rules[elements[0]][elements[1]][elements[2]] = {}
                if int(elements[3].split('.')[0]) not in rules[elements[0]][elements[1]][elements[2]].keys():
                    rules[elements[0]][elements[1]][elements[2]][int(elements[3].split('.')[0])] = {
                        headers[4]: elements[4], headers[5]: eval(elements[5]),
                        headers[6]: elements[6], headers[7]: elements[7]}
        self.log.info("csv rule file {0} successfully parsed".format(f))
        return rules

    def _xlsx_to_csv(self, f, g):
        import xlrd, csv
        wb = xlrd.open_workbook(f)
        sh = wb.sheet_by_name('Sheet1')
        your_csv_file = open(g, 'w')
        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_MINIMAL, delimiter=';')
        for rownum in range(sh.nrows):
            wr.writerow(sh.row_values(rownum))
        your_csv_file.close()
