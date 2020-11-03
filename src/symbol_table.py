#Clase engargada de simular la tabla de símbolos. Cada entrada de la tabla es guardada como una entrada en la clase.
#La clase además contiene métodos adicionales para facilitar la interacción entre la tabla y el analizador léxico.
class SymbolTable:
    def __init__(self, options):
        self.table = []

        self.out_file = options["tables"]

    #Añade una entrada a la tabla de símbolos
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

    #Comprueba si la entrada se encuentra en la tabla, devolviendo true o false.
    def has(self, lexeme):
        for entry in self.table:
            if entry["lexeme"] == lexeme:
                return True

        return False

    #Comprueba si la entrada se encuentra en la tabla y devuelve su posición
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
