from antlr4 import *

from CCodeGen import *
from C_makefile import C_makefile
from lexical_and_syntax_analysis.HelloLexer import HelloLexer
from lexical_and_syntax_analysis.HelloListener import HelloListener
from lexical_and_syntax_analysis.HelloParser import HelloParser

from SemanticAnalyser import SemanticAnalyser


class HelloPrintListener(HelloListener):
    def enterProgram(self, ctx):
        print(ctx.routineDeclaration())


def main():
    lexer = HelloLexer(FileStream('in.txt'))
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.program()
    # printer = HelloPrintListener()
    printer = SemanticAnalyser()
    printer = printer.visit(tree)
    visitor = CCodeGen()
    visitor.visit(tree)
    makefile = C_makefile(visitor.type_def_queue, visitor.queue, visitor.routines)
    makefile.make_file()
    # visitor.visit(tree)


if __name__ == '__main__':
    main()
