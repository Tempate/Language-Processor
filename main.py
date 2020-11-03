from optparse import OptionParser

from src.automata import Automata
from src.symbol_table import SymbolTable


def main():
    options = read_commands()

    symbol_table = SymbolTable(options)

    automata = Automata(options, symbol_table)
    automata.run()

    symbol_table.save()

#Función encargada de gestionar la interacción con el usuario. Le permite al usuario mediante argumentos:
# mostrar la ayuda, elegir el directorio del archivo a leer y el directorio donde guardar los archivos que se generen.
def read_commands():
    parser = OptionParser("%prog -f <input_file>")
    parser.add_option("-f", dest="input", help="File to analyse")
    parser.add_option("-o", dest="output", help="Directory in which to save output files")

    (options, args) = parser.parse_args()

    #Si no se proporcionan argumentos se muestra la ayuda por consola.
    if not options.input:
        parser.print_help()
        exit(0)

    if not options.output:
        options.output = ""
    elif options.output[-1] != "/":
        options.output += "/"

    options = {
        "input" : options.input,
        "tokens": options.output + "tokens.txt",
        "tables": options.output + "tables.txt"
    }

    return options


if __name__ == "__main__":
    main()