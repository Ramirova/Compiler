from HelloVisitor import HelloVisitor
from SymbolTable import SymbolTable


class SymbolTableGenerator(HelloVisitor):
    # symbol_table = SymbolTable()

    def visitProgram(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#simpleDeclaration.
    def visitSimpleDeclaration(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx):
        lang_type = None
        if ctx.lang_type() is not None:
            lang_type = ctx.lang_type()
        if lang_type is not None:
            print("var ", ctx.Identifier(1), ":", lang_type)
        print("var ", ctx.Identifier(2), " is ", ctx.expression(1))
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
        return self.visitChildren(ctx)

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
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#whileLoop.
    def visitWhileLoop(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#forLoop.
    def visitForLoop(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#lang_range.
    def visitLang_range(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#ifStatement.
    def visitIfStatement(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#routineDeclaration.
    def visitRoutineDeclaration(self, ctx):
        return self.visitChildren(ctx)

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
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#relation.
    def visitRelation(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#simple.
    def visitSimple(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#factor.
    def visitFactor(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#summand.
    def visitSummand(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#primary.
    def visitPrimary(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#modifiablePrimary.
    def visitModifiablePrimary(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#eos.
    def visitEos(self, ctx):
        return self.visitChildren(ctx)
