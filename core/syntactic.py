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

    def run(self):
        while self.stack and self.tokens:
            if STATE_PATTERN.match(self.stack[0]):
                rule = self.get_rule()

                if type(rule) != str:
                    raise ValueError("Invalid symbol for rule " + self.stack[0])

                self.stack = self.parse_rule(rule) + self.stack[1:]
            else:
                action = self.stack.pop(0)

                if action == "''":
                    continue

                token = self.tokens.pop(0)

                if action != token.get_symbol():
                    raise ValueError("Token <%s, %d> doesn't match %s" % (token.type, token.attribute, action))

    def get_rule(self):
        row = self.grammar_table[(self.grammar_table["Nonterminal"] == self.stack[0])]
        symbol = self.tokens[0].get_symbol()

        rule = row[symbol].iloc[0]

        self.write_rule_index(row.index[0])

        return rule

    def write_rule_index(self, index):
        self.out_file.write("%d\n" % index)

    @staticmethod
    def parse_rule(rule):
        return rule.split(" -> ")[1].split()
     