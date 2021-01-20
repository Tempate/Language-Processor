from api.tokens import Token
from api.stack import Stack
from api.symbol_table import SymbolTable

import pandas as pd
import re


NON_TERMINAL_STATE_PATTERN = re.compile("^[A-Z]{1,2}$")
SEMANTIC_CODE_PATTERN = re.compile("^{(\d+\.\d+)}$")

INITIAL_STATE = 'O'
BLANK_SYMBOL = "''"
END_OF_FILE_SYMBOL = '$'


widths = {
    "number": 1,
    "boolean": 1,
    "string": 64
}


class SynSemAutomata:
    def __init__(self, options, tokens, symbol_tables):
        self.options = options
        self.tokens = tokens

        self.symbol_tables = symbol_tables
        self.current_table = symbol_tables[0]

        self.grammar_table = pd.read_csv("api/context_free_grammar_table_.csv")
        self.code_table = pd.read_csv("api/semantic_code_table.csv")
        
        self.out_file = open(options["parse"], "w")
        self.out_file.write("Descendente ")


    def run(self):
        stack = Stack()
        stack.add(INITIAL_STATE)

        self.analyse(INITIAL_STATE, stack)


    def analyse(self, symbol, stack):
        if NON_TERMINAL_STATE_PATTERN.match(symbol):
            # The symbol is a non-terminal state
            rule = self.find_rule(symbol)

            for symbol in rule.split():
                
                if symbol == "id":
                    stack.add(str(self.tokens[0].attribute))
                else:
                    stack.add(symbol)
                
                self.analyse(symbol, stack.copy())

        elif SEMANTIC_CODE_PATTERN.match(symbol):
            # The symbol is a pointer to a segment of code
            pointer = SEMANTIC_CODE_PATTERN.match(symbol).group(1)
            code = self.find_code(pointer)

            # Run the code
            exec(code)

        elif symbol != BLANK_SYMBOL:
            # The symbol is a terminal state
            # We make sure the current token matches the symbol

            token = self.tokens.pop(0)

            if symbol != token.get_symbol():
                self.error("Token '%s' doesn't match '%s'" % (token, symbol))


    def find_rule(self, state):
        """ 
        Find the rule for a state and a token 
        If there are no tokens left, use the END_OF_FILE symbol
        """
        state_row = self.grammar_table[(self.grammar_table["Nonterminal"] == state)]
        
        symbol = self.tokens[0].get_symbol() if self.tokens else END_OF_FILE_SYMBOL
        
        cell = state_row[symbol].iloc[0]

        if not cell:
            self.error("Invalid symbol {1} for state {2}".format(symbol, state_row))

        if type(cell) != str:
            self.error("Invalid syntax")

        if '. ' not in cell:
            raise ValueError("Cell doesn't match format: <rule number>. <rule>")

        index, rule = cell.split('. ')

        self.write_rule_index(index)

        return rule.split(' -> ')[1]

    
    def find_code(self, pointer):
        """ Find the semantic action for a pointer """
        return self.code_table[(self.code_table["Pointer"] == float(pointer))]["Code"].iloc[0]


    def find_id(self, id):
        """ Check if it comes from a local or global symbol table """

        try:
            id = int(id)
        except ValueError:
            raise ValueError("%s value is not convertible to int" % str(id))

        symbol_table = self.current_table if id >= 10 else self.symbol_tables[0]
        return symbol_table.table[id % 10]

    
    def error(self, message):
        print("[-] Error: " + message)
        exit(0)
    

    def write_rule_index(self, index):
        self.out_file.write(index + ' ')
     