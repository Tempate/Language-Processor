class SymbolTable:
    def __init__(self, options):
        self.table = []

        self.out_file = options["tables"]

    def add(self, lexeme):
        entry = {
            "lexeme": lexeme,
            "type": "",
            "shift": "",
            "param_count": "",
            "param_type": "",
            "return_type": "",
            "label": ""
        }

        self.table.append(entry)

        return len(self.table) - 1

    def has(self, lexeme):
        for entry in self.table:
            if entry["lexeme"] == lexeme:
                return True

        return False

    def find(self, lexeme):
        for i in range(len(self.table)):
            entry = self.table[i]

            if entry["lexeme"] == lexeme:
                return i

        return -1

    def to_string(self):
        text  = "#1:\n"
        
        for entry in self.table:
            text += "* '%s'\n" % entry["lexeme"]

        return text

    def save(self):
        file = open(self.out_file, "w")
        file.write(self.to_string())
        file.close()
