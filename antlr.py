from antlr4 import *
from HelloLexer import HelloLexer
from HelloListener import HelloListener
from HelloParser import HelloParser
from SymbolTableGenerator import SymbolTableGenerator
import sys


class HelloPrintListener(HelloListener):
    def enterProgram(self, ctx):
        print(ctx.routineDeclaration())


def main():
    lexer = HelloLexer(FileStream('in.txt'))
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.program()
    # printer = HelloPrintListener()
    # printer = SymbolTableGenerator()
    visitor = SymbolTableGenerator()
    visitor.visit(tree)
    # walker = ParseTreeWalker()
    # walker.walk(printer, tree)


if __name__ == '__main__':
    main()
