class SymbolTable:
    def __init__(self, options, id):
        self.id = id
        self.shift = 0

        # Cada entrada de la tabla será un elemento de la lista
        self.table = []

        self.out_file = options["tables"]

    # Añade una entrada a la tabla de símbolos
    def add(self, entry):
        if self.has(entry["lexeme"]):
            self.table[self.find_index(entry["lexeme"])] = self.complete(entry)
        else:
            self.table.append(self.complete(entry))
        
        return len(self.table) - 1

    # Comprueba si la entrada se encuentra en la tabla
    def has(self, lexeme):
        for entry in self.table:
            if entry["lexeme"] == lexeme:
                return True

        return False

    # Devuelve la posición de una entrada en la tabla o -1 si no está
    def find(self, lexeme):
        for entry in self.table:
            if entry["lexeme"] == lexeme:
                return entry

        raise IndexError("Lexeme not in symbol table")

    def find_index(self, lexeme):
        for index in range(len(self.table)):
            if self.table[index]["lexeme"] == lexeme:
                return index

        raise IndexError("Lexeme not in symbol table")

    def set(self, lexeme, attr, value):
        self.table[self.find_index(lexeme)][attr] = value

    def complete(self, entry):
        default = {
            "lexeme": "",
            "type": "",
            "label": "",
            "shift": 0,
            "param_count": 0,
            "param_type": [],
            "return_type": ""
        }

        new_entry = {}

        for key in default:
            new_entry[key] = entry[key] if key in entry else default[key]

        return new_entry

    def __str__(self):
        text  = "#%d:\n" % self.id

        for entry in self.table:
            text += "* LEXEMA: '%s'\n" % entry["lexeme"]
            text += "ATRIBUTOS:\n"

            trans = {
                "type": "Tipo",
                "label": "EtiqFuncion",
                "shift": "Despl",
                "param_count": "numParam",
                "return_type": "TipoRetorno"
            }

            for key in trans:
                if entry[key] or (key == "shift" and entry["type"] != "function"):
                    text += "+ %s : %s \n" % (trans[key], "'%s'" % entry[key].upper() if type(entry[key]) == str else str(entry[key]).upper())

            for i in range(len(entry["param_type"])):
                text += "+ TipoParam%d : '%s'\n" % (i+1, entry["param_type"][i].upper())

            text += "\n"

        return text

    def save(self):
        with open(self.out_file, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(str(self) + '\n' + content)
