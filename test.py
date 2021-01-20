from core.lexical import LexicalAutomata
from core.syntactic import SyntacticAutomata
from api.symbol_table import SymbolTable

import filecmp
import os


def test():
    for i in range(14):
        run(i + 1)


def run(id_):
    dir_ = "tests/test%d/" % id_

    options = {
        "input": dir_ + "test.txt",
        "tokens": dir_ + "tokens.txt", 
        "tables": dir_ + "tables.txt",
        "parse": dir_ + "parse.txt"
    }

    print("\n[*] Running test %d" % id_)

    symbol_table = SymbolTable(options)

    tokens = LexicalAutomata(options, symbol_table).run()
    SyntacticAutomata(options, tokens).run()

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