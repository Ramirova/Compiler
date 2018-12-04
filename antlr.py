from antlr4 import *

from CCodeGen import CCodeGen
from HelloLexer import HelloLexer
from HelloListener import HelloListener
from HelloParser import HelloParser
from C_makefile import C_makefile

from SymbolTableGenerator import SymbolTableGenerator


class HelloPrintListener(HelloListener):
    def enterProgram(self, ctx):
        print(ctx.routineDeclaration())


def main():
    lexer = HelloLexer(FileStream('in.txt'))
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.program()
    # printer = HelloPrintListener()
    printer = SymbolTableGenerator()
    printer = printer.visit(tree)
    visitor = CCodeGen()
    visitor.visit(tree)
    print(visitor.type_def_queue)
    print(visitor.queue)
    print(visitor.routines)
    makefile = C_makefile(visitor.type_def_queue, visitor.queue, visitor.routines)
    makefile.make_file()

if __name__ == '__main__':
    main()
