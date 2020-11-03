from optparse import OptionParser

from automata import Automata
from symbol_table import SymbolTable


def main():
    options = read_commands()

    symbol_table = SymbolTable(options)

    automata = Automata(options, symbol_table)
    automata.run()

    symbol_table.save()


def read_commands():
    parser = OptionParser()
    parser.add_option("-f", dest="input", help="File to analyse")
    parser.add_option("-t", "--output-tokens", dest="output_tokens", help="File to save tokens to")
    parser.add_option("-s", "--output-tables", dest="output_tables", help="File to save tables to")

    (options, args) = parser.parse_args()

    if not options.output_tokens:
        options.output_tokens = "tokens.txt"

    if not options.output_tables:
        options.output_tables = "tables.txt"

    return options


if __name__ == "__main__":
    main()