from .symbol_table import SymbolTable
from .tokens import Token
from .characters import *


class Automata:
    def __init__(self, options, symbol_table):
        self.state = self.state_0

        self.inp_file = open(options["input"], "r")
        self.out_file = open(options["tokens"], "w")

        self.symbol_table = symbol_table

        self.current_line = {"number": 1, "value": ""}
        
        self.value = 0
        self.lexeme = ""
 
    def run(self):
        while True:
            char = self.read_next_character()

            if not char:
                break
            elif char == '\n':
                self.current_line["number"] += 1
                self.current_line["value"] = ""
            else:
                self.current_line["value"] += char

            self.state(char)

        if self.state == self.state_3:
            self.state_9(' ')
        elif self.state == self.state_4:
            self.state_10(' ')

        self.inp_file.close()
        self.out_file.close()

    def state_0(self, char):
        if char in delimiters:
            self.state = self.state_0
        elif char == "-":
            self.state = self.state_1
        elif char in sigma:
            self.state_7(char)
        elif char == "&":
            self.state = self.state_2
        elif char in numbers:
            self.value = int(char)
            self.state = self.state_3
        elif char in letters:
            self.lexeme = char
            self.state = self.state_4
        elif char == "\'":
            self.lexeme = ""
            self.state = self.state_5
        elif char == "/":
            self.state = self.state_12
        else:
            self.invalid_character_error(char)

    def state_1(self, char):
        if char == "=":
            self.state_6(char)
        else:
            self.invalid_character_error(char)

    def state_2(self, char):
        if char == "&":
            self.state_8(char)
        else:
            self.invalid_character_error(char)

    def state_3(self, char):
        if char in numbers:
            self.value = self.value * 10 + int(char)
        elif char in delta:
            self.state_9(char)
        else:
            self.invalid_character_error(char)

    def state_4(self, char):
        valid = numbers + letters + ['_']

        if char in valid:
            self.lexeme += char
        elif char in delta:
            self.state_10(char)
        else:
            self.invalid_character_error(char)

    def state_5(self, char):
        if char == '\'':
            self.state = self.state_11
        else:
            self.lexeme += char
            

    def state_6(self, char):
        token = Token("operadorAsignacion", "2")

        self.write_token(token)
        self.state = self.state_0

    def state_7(self, char):
        token = Token("null", "null")

        if char == '+':
            token = Token("operadorAritmetico", "1")
        elif char == '=':
            token = Token("operadorAsignacion", "1")
        elif char == '<':
            token = Token("operadorRelacional", "1")
        elif char == '(':
            token = Token("separador", "1")
        elif char == ')':
            token = Token("separador", "2")
        elif char == '{':
            token = Token("separador", "3")
        elif char == '}':
            token = Token("separador", "4")
        elif char == ',':
            token = Token("separador", "5")
        elif char == ';':
            token = Token("separador", "6")
        elif char == ':':
            token = Token("separador", "7")
        
        self.write_token(token)
        self.state = self.state_0

    def state_8(self, char):
        token = Token("operadorLogico", "1")

        self.write_token(token)
        self.state = self.state_0

    def state_9(self, char):
        token = Token("constanteEntera", self.value)

        self.write_token(token)
        self.state_0(char)

    def state_10(self, char):
        reserved_words = [
            "function", "let", "number", "boolean", "string", "if", "return", 
            "switch", "case", "default", "break", "alert", "input"
        ]

        if self.lexeme in reserved_words:
            token = Token(self.lexeme, "")
        elif self.lexeme == "true" or self.lexeme == "false":
            token = Token("constanteBooleana", self.lexeme)
        elif not self.symbol_table.has(self.lexeme):
            # TODO: declaration zone
            position = self.symbol_table.add(self.lexeme)
            token = Token("identificador", position)
        else:
            position = self.symbol_table.find(self.lexeme)
            token = Token("identificador", position)

        self.write_token(token)
        self.state_0(char)

    def state_11(self, char):
        token = Token("cadenaCaracteres", self.lexeme)

        self.write_token(token)
        self.state_0(char)

    def state_12(self, char):
        if char == '/':
            self.state = self.state_13
        else:
            self.invalid_character_error(char)

    def state_13(self, char):
        if char == '\n':
            self.state = self.state_0

    def read_next_character(self):
        char = self.inp_file.read(1)

        # We've reached the end of the file
        if not char:
            return 0

        return char

    def write_token(self, token):
        self.out_file.write(token.to_string() + "\n")

    def invalid_character_error(self, char):
        print("\n\033[93m[-] Invalid character\033[0m %s in line %d: \n" % (char, self.current_line["number"]))
        print(self.current_line["value"][:-1] + "\033[91m" + self.current_line["value"][-1] + "\033[0m\n")
        exit(0)
