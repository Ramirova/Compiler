from antlr4 import *

from CCodeGen import *
from C_makefile import C_makefile
from lexical_and_syntax_analysis.HelloLexer import HelloLexer
from lexical_and_syntax_analysis.HelloParser import HelloParser

from SemanticAnalyser import SemanticAnalyser


def main():
    lexer = HelloLexer(FileStream('in.txt'))
    stream = CommonTokenStream(lexer)
    parser = HelloParser(stream)
    tree = parser.program()
    printer = SemanticAnalyser()
    printer = printer.visit(tree)
    visitor = CCodeGen()
    visitor.visit(tree)
    makefile = C_makefile(visitor.type_def_queue, visitor.queue, visitor.routines, visitor.main_allocs)
    makefile.make_file()


if __name__ == '__main__':
    main()
