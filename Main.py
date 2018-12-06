from antlr4 import *

from CCodeGen import *
from C_makefile import C_makefile
from lexical_and_syntax_analysis.HelloLexer import HelloLexer
from lexical_and_syntax_analysis.HelloParser import HelloParser

from SemanticAnalyser import SemanticAnalyser


def main():
    print("Starting lexical analysis...\n")
    lexer = HelloLexer(FileStream('in.txt'))
    print("Lexical analysis is done!\n")
    stream = CommonTokenStream(lexer)
    print("Starting syntax analysis...\n")
    parser = HelloParser(stream)
    tree = parser.program()
    print("Syntax analysis is done!\n")
    printer = SemanticAnalyser()
    print("Starting semantic analysis...\n")
    printer = printer.visit(tree)
    print("Semantic analysis is done...\n")
    visitor = CCodeGen()
    visitor.visit(tree)
    print(visitor.queue)
    makefile = C_makefile(visitor.type_def_queue, visitor.queue, visitor.routines, visitor.main_allocs)
    makefile.make_file()


if __name__ == '__main__':
    main()
