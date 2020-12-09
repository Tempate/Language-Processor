from api.tokens import Token

import pandas as pd
import re


STATE_PATTERN = re.compile("^[A-Z]{1,2}$")
INITIAL_STATE = 'O'


class SyntacticAutomata:
    def __init__(self, options, tokens):
        self.stack = [INITIAL_STATE]
        self.tokens = tokens

        self.grammar_table = pd.read_csv("api/context_free_grammar_table.csv")
        self.out_file = open(options["parse"], "w")

        self.out_file.write("Descendente ")


    def run(self):
        while self.stack:
            if STATE_PATTERN.match(self.stack[0]):
                index, rule = self.get_rule()

                if type(rule) != str:
                    raise ValueError("Invalid symbol for rule " + str(index))

                self.stack = rule.split() + self.stack[1:]
            else:
                action = self.stack.pop(0)

                if action == "''":
                    continue

                token = self.tokens.pop(0)

                if action != token.get_symbol():
                    raise ValueError("Token <%s, %d> doesn't match %s" % (token.type, token.attribute, action))


    def get_rule(self):
        row = self.grammar_table[(self.grammar_table["Nonterminal"] == self.stack[0])]
        symbol = self.tokens[0].get_symbol() if self.tokens else '$'
        
        index, rule = row[symbol].iloc[0].split(". ")

        self.write_rule_index(index)

        return index, rule


    def write_rule_index(self, index):
        self.out_file.write("%d " % int(index))
     