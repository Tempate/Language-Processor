from src.automata import Automata
from src.symbol_table import SymbolTable

import filecmp
import os

def test():
    for i in range(5):
        run(i + 1)


def run(id_):
    dir_ = "tests/test%d/" % id_

    options = {
        "input": dir_ + "test.txt",
        "tokens": "tokens.txt", 
        "tables": "tables.txt"
    }

    print("\n[*] Running test %d" % id_)

    symbol_table = SymbolTable(options)

    automata = Automata(options, symbol_table)
    automata.run()

    symbol_table.save()

    show_result("Tokens", dir_, options["tokens"])
    show_result("Tables", dir_, options["tables"])


def show_result(label, dir_, file):
    if filecmp.cmp(file, dir_ + file):
        print("\t[+] %s: Passed" % label)
    else:
        print("\t[-] %s: Failed" % label)

    os.remove(file)


if __name__ == "__main__":
    test()