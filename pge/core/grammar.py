from core.utilities import ordered_set
import json
import re

class Grammar:
    """Class that represents a grammar. It works with the prefix notation."""
    NT = "NT"
    T = "T"
    NT_PATTERN = "(<.+?>)"
    RULE_SEPARATOR = "::="
    PRODUCTION_SEPARATOR = "|"

    def __init__(self):
        self.grammar = {}
        self.grammar_file = None
        self.non_terminals, self.terminals = set(), set()
        self.ordered_non_terminals = ordered_set.OrderedSet()
        self.non_recursive_options = {}
        self.number_of_options_by_non_terminal = None
        self.start_rule = None
        self.counter = {}

    def set_path(self, grammar_path):
        self.grammar_file = grammar_path

    def get_non_recursive_options(self):
        return self.non_recursive_options

    def read_grammar(self):
        """
        Reads a Grammar in the BNF format and converts it to a python dictionary
        This method was adapted from PonyGE version 0.1.3 by Erik Hemberg and James McDermott
        If the file extension is .json, it will be directly loaded.
        """
        if self.grammar_file is None:
            raise Exception("You need to specify the path of the grammar file")

        if self.grammar_file.endswith("json"):
            with open(self.grammar_file) as f:
                self.grammar = json.load(f)
            # assumes that the first key of the dictionary is the axiom
            self.start_rule = list(self.grammar.keys())[0]
            self.ordered_non_terminals = list(self.grammar.keys())
        else:
            with open(self.grammar_file, "r") as f:
                for line in f:
                    if not line.startswith("#") and line.strip() != "":
                        if line.find(self.PRODUCTION_SEPARATOR):
                            left_side, productions = line.split(self.RULE_SEPARATOR)
                            left_side = left_side.strip()
                            if not re.search(self.NT_PATTERN, left_side):
                                raise ValueError("Left side not a non-terminal!")
                            self.non_terminals.add(left_side)
                            self.ordered_non_terminals.add(left_side)
                            # assumes that the first rule in the file is the axiom
                            if self.start_rule is None:
                                self.start_rule = left_side
                            temp_productions = []
                            prob = 1.0/len(productions.split(self.PRODUCTION_SEPARATOR))
                            for production in [production.strip() for production in productions.split(self.PRODUCTION_SEPARATOR)]:
                                productions_probs = []
                                temp_production = []
                                if not re.search(self.NT_PATTERN, production):
                                    if production == "None":
                                        production = ""
                                    self.terminals.add(production)
                                    temp_production.append((production, self.T))
                                else:
                                    for value in re.findall("<.+?>|[^<>]*", production):
                                        if value != "":
                                            if re.search(self.NT_PATTERN, value) is None:
                                                sym = (value, self.T)
                                                self.terminals.add(value)
                                            else:
                                                sym = (value, self.NT)
                                            temp_production.append(sym)
                                productions_probs.append(temp_production)
                                productions_probs.append(prob)
                                temp_productions.append(productions_probs)
                            if left_side not in self.grammar:
                                self.grammar[left_side] = temp_productions
        self.compute_non_recursive_options()
        self.counter = dict.fromkeys(self.grammar.keys(),[])
        for k in self.counter.keys():
            self.counter[k] = [0] * len(self.grammar[k])

    def get_counter(self):
        return self.counter

    def get_non_terminals(self):
        return self.ordered_non_terminals

    def count_number_of_options_in_production(self):
        if self.number_of_options_by_non_terminal is None:
            self.number_of_options_by_non_terminal = {}
            for nt in self.ordered_non_terminals:
                self.number_of_options_by_non_terminal.setdefault(nt, len(self.grammar[nt]))
        return self.number_of_options_by_non_terminal

    def compute_non_recursive_options(self):
        self.non_recursive_options = {}
        for nt in self.ordered_non_terminals:
            choices = []
            for nrp in self.list_non_recursive_productions(nt):
                choices.append(self.grammar[nt].index(nrp))
            self.non_recursive_options[nt] = choices

    def list_non_recursive_productions(self, nt):
        non_recursive_elements = []
        for options in self.grammar[nt]:
            for option in options[0]:
                if option[1] == self.NT and option[0] == nt:
                    break
            else:
                non_recursive_elements += [options]
        return non_recursive_elements

    def is_individual_t(self, phenotype):
        # check if some individual only has terminal symbols
        for symbol in phenotype:
            if symbol in self.ordered_non_terminals:
                return False
        return True

    def get_start_rule(self):
        return self.start_rule

    def get_dict(self):
        return self.grammar

    def get_grammar_file(self):
        return self.grammar_file
    
    @staticmethod
    def python_filter(txt):
        """ Create correct python syntax.
        We use {: and :} as special open and close brackets, because
        it's not possible to specify indentation correctly in a BNF
        grammar without this type of scheme."""
        txt = txt.replace("\le", "<=")
        txt = txt.replace("\ge", ">=")
        txt = txt.replace("\l", "<")
        txt = txt.replace("\g", ">")
        txt = txt.replace("\eb", "|")
        indent_level = 0
        tmp = txt[:]
        i = 0
        while i < len(tmp):
            tok = tmp[i:i+2]
            if tok == "{:":
                indent_level += 1
            elif tok == ":}":
                indent_level -= 1
            tabstr = "\n" + "  " * indent_level
            if tok == "{:" or tok == ":}" or tok == "\\n":
                tmp = tmp.replace(tok, tabstr, 1)
            i += 1
            # Strip superfluous blank lines.
            txt = "\n".join([line for line in tmp.split("\n") if line.strip() != ""])
        return txt


    def __str__(self):
        grammar = self.grammar
        text = ""
        for key in self.ordered_non_terminals:
            text += key + " ::= "
            for options in grammar[key]:
                for option in options:
                    text += option[0]
                if options != grammar[key][-1]:
                    text += " | "
            text += "\n"
        return text

# Create one instance and export its methods as module-level functions.
# The functions share state across all uses
# (both in the user's code and in the Python libraries), but that's fine
# for most programs and is easier for the casual user


_inst = Grammar()
set_path = _inst.set_path
read_grammar = _inst.read_grammar
get_non_terminals = _inst.get_non_terminals
count_number_of_options_in_production = _inst.count_number_of_options_in_production
compute_non_recursive_options = _inst.compute_non_recursive_options
list_non_recursive_productions = _inst.list_non_recursive_productions
start_rule = _inst.get_start_rule
get_non_recursive_options = _inst.get_non_recursive_options
get_dict = _inst.get_dict
get_counter = _inst.get_counter
ordered_non_terminals = _inst.ordered_non_terminals
python_filter = _inst.python_filter
is_individual_t = _inst.is_individual_t
get_grammar_file = _inst.get_grammar_file
