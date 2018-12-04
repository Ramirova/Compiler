from antlr4 import *

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
    # visitor = CCodeGen([])
    # visitor.visit(tree)
    # walker = ParseTreeWalker()
    # walker.walk(printer, tree)


if __name__ == '__main__':
    main()
