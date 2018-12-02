from HelloVisitor import HelloVisitor
from SymbolTable import SymbolTable
from HelloParser import HelloParser
from TypeTable import *
import unicodedata


class SymbolTableGenerator(HelloVisitor):
    current_symbol_table = SymbolTable(parent=None)


    def visitProgram(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#simpleDeclaration.
    def visitSimpleDeclaration(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx):
        identifier = ctx.Identifier().getText()
        identifier = unicodedata.normalize('NFKD', identifier).encode('ascii', 'ignore')
        lang_type = self.visitLang_type(ctx)
        self.current_symbol_table.add(identifier, lang_type)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx):
        print("type ", ctx.Identifier(), ' is ', ctx.lang_type())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#lang_type.
    def visitLang_type(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#primitiveType.
    def visitPrimitiveType(self, ctx):
        c = ctx.children[0].getText()
        c = unicodedata.normalize('NFKD', c).encode('ascii', 'ignore')
        return c

    # Visit a parse tree produced by HelloParser#userType.
    def visitUserType(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#recordType.
    def visitRecordType(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#arrayType.
    def visitArrayType(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#statement.
    def visitStatement(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#assignment.
    def visitAssignment(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#routineCall.
    def visitRoutineCall(self, ctx):
        routine_name = ctx.Identifier().getText()
        routine_name = unicodedata.normalize('NFKD', routine_name).encode('ascii', 'ignore')
        if not self.current_symbol_table.routine_defined_in_scope(routine_name):
            raise Exception('Routine {} is not defined'.format(routine_name))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#whileLoop.
    def visitWhileLoop(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#forLoop.
    def visitForLoop(self, ctx):
        identifier = ctx.Identifier().getText()
        identifier = unicodedata.normalize('NFKD', identifier).encode('ascii', 'ignore')
        if not self.current_symbol_table.is_defined_in_scope(identifier):
            raise Exception('Variable {} is not defined'.format(identifier))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#lang_range.
    def visitLang_range(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#ifStatement.
    def visitIfStatement(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#routineDeclaration.
    def visitRoutineDeclaration(self, ctx):
        identifier = unicodedata.normalize('NFKD', ctx.Identifier().getText()).encode('ascii', 'ignore')
        self.current_symbol_table.add_routine(identifier)
        self.current_symbol_table = self.current_symbol_table.create_child_scope(identifier)
        peremennaya = self.visitChildren(ctx)
        self.current_symbol_table = self.current_symbol_table.parent_scope
        return peremennaya

    # Visit a parse tree produced by HelloParser#parameters.
    def visitParameters(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx):

        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#body.
    def visitBody(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#expression.
    def visitExpression(self, ctx):
        type = 'boolean'
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#relation.
    def visitRelation(self, ctx):
        type = 'boolean'
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#simple.
    def visitSimple(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#factor.
    def visitFactor(self, ctx):
        children = ctx.children
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#summand.
    def visitSummand(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#primary.
    def visitPrimary(self, ctx):
        children = ctx.children

        int_lit = ctx.IntegerLiteral()
        float_lit = ctx.RealLiteral()

        is_int_lit = False
        is_real_lit = False
        is_boolean_lit = False

        if int_lit is not None:
            is_int_lit = True
        elif float_lit is not None:
            is_real_lit = True
        elif unicodedata.normalize('NFKD', children[0].getText()).encode('ascii',
                                                                         'ignore') == 'true' or unicodedata.normalize(
            'NFKD', children[0].getText()).encode('ascii', 'ignore') == 'false':
            is_boolean_lit = True

        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#modifiablePrimary.
    def visitModifiablePrimary(self, ctx):
        children = ctx.children

        identifier = None
        array_identifier = None
        function_calls = []

        if len(children) == 1:
            identifier = children[0].getText()
            identifier = unicodedata.normalize('NFKD', identifier).encode('ascii', 'ignore')
            if not self.current_symbol_table.is_defined_in_scope(identifier):
                raise Exception('Variable {} is not defined'.format(identifier))
            # return identifier
        elif type(children[2]) is HelloParser.ExpressionContext:
            array_identifier = children[0].getText()
            array_identifier = unicodedata.normalize('NFKD', array_identifier).encode('ascii', 'ignore')
        else:
            for i in range(len(children)):
                if i % 2 == 0:
                    id = children[i].getText()
                    id = unicodedata.normalize('NFKD', id).encode('ascii', 'ignore')
                    function_calls.append(id)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#eos.
    def visitEos(self, ctx):
        return self.visitChildren(ctx)
