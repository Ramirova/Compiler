from antlr4 import *
from HelloLexer import HelloLexer
from HelloListener import HelloListener
from HelloParser import HelloParser
import sys


class HelloPrintListener(HelloListener):
    def enterProgram(self, ctx):
        print(ctx.simpleDeclaration())


def main():
    lexer = HelloLexer(FileStream('in.txt'))
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.program()
    printer = HelloPrintListener()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)


if __name__ == '__main__':
    main()
