from optparse import OptionParser

from core.lexical import LexicalAutomata
from core.syntactic import SyntacticAutomata
from api.symbol_table import SymbolTable


def main():
    options = read_commands()

    symbol_table = SymbolTable(options)

    tokens = LexicalAutomata(options, symbol_table).run()
    SyntacticAutomata(options, tokens).run()

    symbol_table.save()


def read_commands():
    parser = OptionParser("%prog -f <input_file>")
    parser.add_option("-f", dest="input", help="File to analyse")
    parser.add_option("-o", dest="output", help="Directory in which to save output files")

    (options, args) = parser.parse_args()

    # Mostrar los ayuda si no se especifica el archivo a leer
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
        "tables": options.output + "tables.txt",
        "parse":  options.output + "parse.txt"
    }

    return options


if __name__ == "__main__":
    main()