class Token:
    def __init__(self, type, attribute):
        self.type = type
        self.attribute = attribute

    def to_string(self):
        return "<" + self.type + ", " + str(self.attribute) + ">"

    def get_symbol(self):
        token_to_symbol = {
            "operadorAsignacion": ['=', '-='],
            "operadorAritmetico": ['+'],
            "operadorRelacional": ['<'],
            "operadorLogico": ['&&'],
            "separador": ['(', ')', '{', '}', ',', ';', ':']
        }

        token_to_id = {
            "constanteEntera":   'c',
            "constanteBooleana": 'c',
            "cadenaCaracteres":  'c',
            "identificador": 'id'
        }

        if self.type in token_to_symbol:
            return token_to_symbol[self.type][self.attribute - 1]
        elif self.type in token_to_id:
            return token_to_id[self.type]

        return self.type
