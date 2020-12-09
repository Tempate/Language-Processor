from api.tokens import Token

import pandas as pd
import re


NON_TERMINAL_STATE_PATTERN = re.compile("^[A-Z]{1,2}$")

INITIAL_STATE = 'O'
BLANK_SYMBOL = "''"
END_OF_FILE_SYMBOL = '$'


class SyntacticAutomata:
    def __init__(self, options, tokens):
        self.stack = [INITIAL_STATE]
        self.tokens = tokens

        self.grammar_table = pd.read_csv("api/context_free_grammar_table.csv")
        
        self.out_file = open(options["parse"], "w")
        self.out_file.write("Descendente ")


    def run(self):
        while self.stack:
            state = self.stack.pop(0)

            if NON_TERMINAL_STATE_PATTERN.match(state):
                rule = self.apply_rule(state)
                self.stack = rule.split() + self.stack

            elif state != BLANK_SYMBOL:
                # The state is terminal
                token = self.tokens.pop(0)

                if state != token.get_symbol():
                    raise ValueError("Token %s doesn't match %s" % (token, action))


    def apply_rule(self, state):
        state_row = self.grammar_table[(self.grammar_table["Nonterminal"] == state)]
        
        # If there are no tokens left, use the END_OF_FILE_SYMBOL
        token_symbol = self.tokens[0].get_symbol() if self.tokens else END_OF_FILE_SYMBOL
        
        cell = state_row[token_symbol].iloc[0]

        # Raise an error when the cell is blank
        if not cell:
            raise ValueError("Invalid symbol {1} for state {2}".format(token_symbol, state_row))

        if '. ' not in cell:
            raise ValueError("Cell doesn't match format: <rule number>. <rule>")

        index, rule = cell.split('. ')

        self.write_rule_index(index)

        return rule


    def write_rule_index(self, index):
        self.out_file.write(index + ' ')
     