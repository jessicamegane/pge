import json
import re

class Grammar:
    def __init__(self):
        self.start = None
        self.nonterminal = []
        self.rules = {}
        self.counter = {}
        self.file_path = None
        # self.load_grammar()

    def set_path(self, path):
        self.file_path = path
    
    def read_grammar(self):
        """ Function to load the grammar. If the file extension is .json, it will be directly loaded."""
        if "json" in self.file_path:
            with open(self.file_path) as f:
                self.rules = json.load(f)['grammar']
            # assumes that the first key of the dictionary is the axiom
            for k,v in self.rules.items():
                if not self.start:
                    self.start = k
                self.counter[k] = [0] * len(v)
                if k not in self.nonterminal:
                    self.nonterminal.append(k)
        else:
            self.load_grammar()

    def load_grammar(self):
        f = open(self.file_path,"r")

        re_expansion = " ::= "
        re_rules_separator = "\|"
        re_rules = "(<[^<>]+>)|([^<>|]+)"
        temp = f.read().splitlines()
        for line in temp:
            line = re.split(re_expansion, line)
            if self.start == None:
                self.start = line[0]
            if line[0] not in self.rules:
                self.rules[line[0]] = []
            if line[0] not in self.counter:
                self.counter[line[0]] = []

            productions = re.split(re_rules_separator, line[1])
            # assign equal probabilities to each production rule of each non terminal
            prob = 1.0/len(productions)
            for prod in productions:
                p = []
                if re.search(re_rules, prod):
                    # TODO: checkar esta parte do codigo 
                    a = re.findall(re_rules, prod)
                    for nt,t in a:
                        if nt != "":
                            p.append(nt)
                            if nt not in self.nonterminal:
                                self.nonterminal.append(nt)
                list_prob = [p, prob]
                self.rules[line[0]].append(list_prob)
            self.counter[line[0]] = [0] * len(productions)

    def get_start(self):
        return self.start

    def rules_NTerminal(self, nt):
        # function that returns rules of some non terminal
        return self.rules[nt]

    def is_NTerminal(self, symbol):
        if symbol in self.nonterminal:
            return True
        return False

    def is_individual_t(self, ind):
        # check if some individual only has terminal symbols
        for symbol in ind:
            if self.is_NTerminal(symbol):
                return False
        return True

    def get_counter(self):
        return self.counter
    
    def get_rules(self):
        return self.rules


_inst = Grammar()
read_grammar = _inst.read_grammar
set_path = _inst.set_path
get_start = _inst.get_start
get_counter = _inst.get_counter
is_individual_t = _inst.is_individual_t
is_NTerminal = _inst.is_NTerminal
rules_NTerminal = _inst.rules_NTerminal
get_dict = _inst.rules