from unittest import TestCase
from antlr4 import *
from CCodeGen import *
from C_makefile import C_makefile
from SemanticAnalyser import SemanticAnalyser
from lexical_and_syntax_analysis.HelloLexer import HelloLexer
from lexical_and_syntax_analysis.HelloListener import HelloListener
from lexical_and_syntax_analysis.HelloParser import HelloParser

class TestCCodeGen(TestCase):


    def test_visitProgram(self):
        lexer = HelloLexer(FileStream('test_program.txt'))
        stream = CommonTokenStream(lexer)
        parser = HelloParser(stream)
        tree = parser.program()
        printer = SemanticAnalyser()
        printer = printer.visit(tree)
        codegen = CCodeGen()
        codegen.visit(tree)
        result = ['void bubble_sort(int l, bool p) {\n', 'int arr[3];\n', '}\n']
        self.assertEqual(codegen.queue, result)

    # def test_visitSimpleDeclaration(self):
    #     self.fail()
    #
    def test_visitVariableDeclaration(self):
        self.fail()
    #
    # def test_getVariableType(self):
    #     self.fail()
    #
    # def test_getArraySize(self):
    #     self.fail()
    #
    # def test_visitTypeDeclaration(self):
    #     self.fail()
    #
    # def test_visitLang_type(self):
    #     self.fail()
    #
    # def test_visitPrimitiveType(self):
    #     self.fail()
    #
    # def test_visitUserType(self):
    #     self.fail()
    #
    # def test_visitRecordType(self):
    #     self.fail()
    #
    # def test_visitArrayType(self):
    #     self.fail()
    #
    # def test_visitStatement(self):
    #     self.fail()
    #
    # def test_visitAssignment(self):
    #     self.fail()
    #
    def test_visitRoutineCall(self):
        self.fail()

    def test_visitWhileLoop(self):
        self.fail()

    def test_visitForLoop(self):
        self.fail()

    # def test_visitLang_range(self):
    #     self.fail()
    #
    # def test_visitIfStatement(self):
    #     self.fail()
    #
    def test_visitRoutineDeclaration(self):
        self.fail()
    #
    # def test_visitParameters(self):
    #     self.fail()
    #
    # def test_visitParameterDeclaration(self):
    #     self.fail()
    #
    def test_visitBody(self):
        self.fail()
    #
    # def test_expressionToString(self):
    #     self.fail()
    #
    def test_visitExpression(self):
        self.fail()
    #
    # def test_visitRelation(self):
    #     self.fail()
    #
    # def test_visitSimple(self):
    #     self.fail()
    #
    # def test_visitFactor(self):
    #     self.fail()
    #
    # def test_visitSummand(self):
    #     self.fail()
    #
    # def test_visitPrimary(self):
    #     self.fail()
    #
    # def test_visitModifiablePrimary(self):
    #     self.fail()
    #
    # def test_visitEos(self):
    #     self.fail()
