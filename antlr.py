import antlr4
from HelloLexer import HelloLexer
from HelloListener import HelloListener
from HelloParser import HelloParser
from SemanticAnalyser import SemanticAnalyser
from SymbolTableGenerator import SymbolTableGenerator

import sys


class HelloPrintListener(HelloListener):
    def enterProgram(self, ctx):
        print(ctx.routineDeclaration())


def main():
    lexer = HelloLexer(antlr4.FileStream('in.txt'))
    stream = antlr4.CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.program()
    # printer = HelloPrintListener()
    # printer = SymbolTableGenerator()
    symbol_table = SymbolTableGenerator.symbol_table
    visitor = SemanticAnalyser(symbol_table)
    visitor.visit(tree)
    # walker = ParseTreeWalker()
    # walker.walk(printer, tree)


if __name__ == '__main__':
    main()
