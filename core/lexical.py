from api.symbol_table import SymbolTable
from api.tokens import Token
from api.characters import *


class LexicalAutomata:
    def __init__(self, options, symbol_tables):
        # Iniciamos el autómata en el estado 0
        self.state = self.state_0

        self.inp_file = open(options["input"], "r")
        self.out_file = open(options["tokens"], "w")

        self.options = options

        self.symbol_tables = symbol_tables
        self.current_table = self.symbol_tables[0]

        self.wants_to_change = False
        self.declaration_zone = False

        self.current_line = {"number": 1, "value": ""}
        
        self.value = 0
        self.lexeme = ""

        self.tokens = []
 
    # Primero leemos el cáracter del documento y luego iniciamos el autómata en 
    # el estado que corresponde pasando el 'char' como parámetro.
    # Durante la ejecución del autómata cambiamos la función a la que hace referencia 
    # "self.state" para simular la transición de estados. 
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

        # Cuando el documento acaba en los estados 3 o 4 ejecutamos sus respectivos estados finales 
        # para reconocer la palabra y generar el token.
        if self.state == self.state_3:
            self.state_9(' ')
        elif self.state == self.state_4:
            self.state_10(' ')
        
        if self.state == self.state_5:
            print("[-] Error: String quotes not closed correctly")
            exit(0)

        self.inp_file.close()
        self.out_file.close()

        return self.tokens
    
    # Los estados de transición procesan el caracter leído. 
    # Los estados finales generan los tokens correspondientes y, 
    # si fuera necesario, se interactúa con la tabla de símbolos.

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
            self.state = self.state_3
        elif char in delta:
            self.state_9(char)
        else:
            self.invalid_character_error(char)
    
    def state_4(self, char):
        valid = numbers + letters + ['_']

        if char in valid:
            self.lexeme += char
            self.state = self.state_4
        elif char in delta:
            self.state_10(char)
        else:
            self.invalid_character_error(char)
    
    def state_5(self, char):
        if char == '\'':
            self.state = self.state_11
        else:
            self.lexeme += char
            self.state = self.state_5
            
    
    def state_6(self, char):
        token = Token("operadorAsignacion", 2)

        self.write_token(token)
        self.state = self.state_0
    
    def state_7(self, char):
        token = Token("null", "null")

        if char == '+':
            token = Token("operadorAritmetico", 1)
        elif char == '=':
            token = Token("operadorAsignacion", 1)
        elif char == '<':
            token = Token("operadorRelacional", 1)
        elif char == '(':
            token = Token("separador", 1)
        elif char == ')':
            token = Token("separador", 2)
        elif char == '{':
            token = Token("separador", 3)
            self.declaration_zone = False
        elif char == '}':
            token = Token("separador", 4)
        elif char == ',':
            token = Token("separador", 5)
        elif char == ';':
            token = Token("separador", 6)
            self.declaration_zone = False

            if self.wants_to_change:
                self.current_table = self.symbol_tables[0]
                self.wants_to_change = False
        elif char == ':':
            token = Token("separador", 7)
        
        self.write_token(token)
        self.state = self.state_0
    
    def state_8(self, char):
        token = Token("operadorLogico", 1)

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

            if self.lexeme == "function":
                self.symbol_tables.append(SymbolTable(self.options, len(self.symbol_tables) + 1))
                self.wants_to_change = True
                self.declaration_zone = True
            elif self.lexeme == "return":
                self.wants_to_change = True
            elif self.lexeme in "let":
                self.declaration_zone = True

        elif self.lexeme == "true" or self.lexeme == "false":
            token = Token("constanteBooleana", self.lexeme)
        elif self.declaration_zone and not self.current_table.has(self.lexeme):
            # El lexema no está en la tabla de símbolos
            position = self.current_table.add({"lexeme": self.lexeme})
            token = Token("identificador", self.gen_id(self.current_table, position))

            if self.wants_to_change:
                if self.current_table == self.symbol_tables[0]:
                    self.current_table = self.symbol_tables[-1]
                else:
                    self.current_table = self.symbol_tables[0]
                
                self.wants_to_change = False

        else:

            try:
                position = self.current_table.find_index(self.lexeme)
                token = Token("identificador", self.gen_id(self.current_table, position))
            except IndexError:
                try:
                    position = self.symbol_tables[0].find_index(self.lexeme)
                    token = Token("identificador", self.gen_id(self.symbol_tables[0], position))
                except IndexError:
                    print("[-] ERROR: variable '%s' is not defined" % self.lexeme)
                    exit(0)

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

    @staticmethod
    def gen_id(table, position):
        return 10 * (table.id - 1) + position

    def read_next_character(self):
        char = self.inp_file.read(1)

        if not char:
            # Final del documento
            return 0

        return char

    def write_token(self, token):
        self.out_file.write("%s\n" % token)
        self.tokens.append(token)

    def invalid_character_error(self, char):
        print("\n\033[93m[-] Invalid character\033[0m %s in line %d: \n" % (char, self.current_line["number"]))
        print(self.current_line["value"][:-1] + "\033[91m" + self.current_line["value"][-1] + "\033[0m\n")
        exit(0)
