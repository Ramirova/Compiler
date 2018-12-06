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
        lexer = HelloLexer(FileStream('TestFiles/test_program.txt'))
        stream = CommonTokenStream(lexer)
        parser = HelloParser(stream)
        tree = parser.program()
        printer = SemanticAnalyser()
        printer = printer.visit(tree)
        codegen = CCodeGen()
        codegen.visit(tree)
        result = ['void sort() {\n', 'int start_loop = 1;\n', '}\n', 'void start_program() {\n', 'int* b = malloc ((3+1)*sizeof(int));\n', '}\n']
        self.assertEqual(codegen.queue, result)

    # def test_visitSimpleDeclaration(self):
    #     self.fail()
    #
    def test_visitVariableDeclaration(self):
        lexer = HelloLexer(FileStream('TestFiles/test_variable_declaration.txt'))
        stream = CommonTokenStream(lexer)
        parser = HelloParser(stream)
        tree = parser.program()
        printer = SemanticAnalyser()
        printer = printer.visit(tree)
        codegen = CCodeGen()
        codegen.visit(tree)
        result = ['int a = 0;\n']
        self.assertEqual(codegen.queue, result)
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
        lexer = HelloLexer(FileStream('TestFiles/test_routine_call.txt'))
        stream = CommonTokenStream(lexer)
        parser = HelloParser(stream)
        tree = parser.program()
        printer = SemanticAnalyser()
        printer = printer.visit(tree)
        codegen = CCodeGen()
        codegen.visit(tree)
        result = ['%d plus_int(%d a, %d b) {\n', 'return a+b;\n', '}\n', 'void calculator(%d a, %d b) {\n', 'int res1 = plus_int(a,b);\n', 'printf("%d", ', 'res1', ');\n', 'printf("%s", "\\n");\n', '}\n']
        self.assertEqual(codegen.queue, result)

    def test_visitWhileLoop(self):
        lexer = HelloLexer(FileStream('TestFiles/test_whileloop.txt'))
        stream = CommonTokenStream(lexer)
        parser = HelloParser(stream)
        tree = parser.program()
        printer = SemanticAnalyser()
        printer = printer.visit(tree)
        codegen = CCodeGen()
        codegen.visit(tree)
        result = ['void plus_whileloop(%d a, %d b) {\n', 'while (a<b) {', 'a = a+1;\n', '}\n', '}\n']
        self.assertEqual(codegen.queue, result)

    def test_visitForLoop(self):
        lexer = HelloLexer(FileStream('TestFiles/test_forloop.txt'))
        stream = CommonTokenStream(lexer)
        parser = HelloParser(stream)
        tree = parser.program()
        printer = SemanticAnalyser()
        printer = printer.visit(tree)
        codegen = CCodeGen()
        codegen.visit(tree)
        result = ['sorting_array_type my_array;\n', 'void bubble_sort(sorting_array_type* b) {\n', 'int start_loop = 1;\n', 'int end_loop = 3;\n', 'int start_second_loop = 1;\n', 'int end_second_loop = 3;\n', 'int temp = 0;\n', '\nfor (int j = start_loop; j <= end_loop; j++) {\n', 'int a = 0;\n', '}\n', '}\n']
        self.assertEqual(codegen.queue, result)

    # def test_visitLang_range(self):
    #     self.fail()
    #
    # def test_visitIfStatement(self):
    #     self.fail()
    #
    def test_visitRoutineDeclaration(self):
        lexer = HelloLexer(FileStream('TestFiles/test_routine_declaration.txt'))
        stream = CommonTokenStream(lexer)
        parser = HelloParser(stream)
        tree = parser.program()
        printer = SemanticAnalyser()
        printer = printer.visit(tree)
        codegen = CCodeGen()
        codegen.visit(tree)
        result = ['void print_numbers(%d start_range, %d end_range) {\n', '\nfor (int i = start_range; i <= end_range; i++) {\n', 'printf("%d", ', 'i', ');\n', 'printf("%s", "\\n");\n', '}\n', '}\n']
        self.assertEqual(codegen.queue, result)
    #
    # def test_visitParameters(self):
    #     self.fail()
    #
    # def test_visitParameterDeclaration(self):
    #     self.fail()
    #
    def test_visitBody(self):
        lexer = HelloLexer(FileStream('TestFiles/test_body.txt'))
        stream = CommonTokenStream(lexer)
        parser = HelloParser(stream)
        tree = parser.program()
        printer = SemanticAnalyser()
        printer = printer.visit(tree)
        codegen = CCodeGen()
        codegen.visit(tree)
        result = ['void start() {\n', 'int* b = malloc ((3+1)*sizeof(int));\n', '}\n']
        self.assertEqual(codegen.queue, result)
    #
    # def test_expressionToString(self):
    #     self.fail()
    #
    def test_visitExpression(self):
        lexer = HelloLexer(FileStream('TestFiles/test_expression.txt'))
        stream = CommonTokenStream(lexer)
        parser = HelloParser(stream)
        tree = parser.program()
        printer = SemanticAnalyser()
        printer = printer.visit(tree)
        codegen = CCodeGen()
        codegen.visit(tree)
        result = ['%d plus(%d a, %d b) {\n', 'return a+b;\n', '}\n']
        self.assertEqual(codegen.queue, result)
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
