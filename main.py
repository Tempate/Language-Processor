from optparse import OptionParser

from core.lexical import LexicalAutomata
from core.synsem import SynSemAutomata

from api.symbol_table import SymbolTable


def main():
    options = read_commands()

    with open(options["tables"], "r+") as file:
        file.seek(0)
        file.truncate()

    symbol_tables = [SymbolTable(options, 1)]

    tokens = LexicalAutomata(options, symbol_tables).run()
    SynSemAutomata(options, tokens, symbol_tables).run()

    symbol_tables[0].save()


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