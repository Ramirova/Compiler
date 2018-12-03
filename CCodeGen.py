from HelloVisitor import HelloVisitor
from SymbolTable import *
from TypeTable import *
import unicodedata


class CCodeGen(HelloVisitor):
    c_type_map = {
        "integer": "int",
        "real": "double",
        "boolean": "bool",
    }

    primitive_type_map = {
        1: "int",
        2: "double",
        3: "bool"
    }

    def __init__(self, args):
        self.current_scope = SymbolTable.root_table
        self.type_table = TypeTable.table
        self.alias_list = []
        self.type_def_queue = []
        self.queue = []

    def visitProgram(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#simpleDeclaration.
    def visitSimpleDeclaration(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx):
        identifier = ctx.Identifier().getText()
        identifier = unicodedata.normalize('NFKD', identifier).encode('ascii', 'ignore')
        SymbolTable.root_table
        type_id = self.current_scope.scope[identifier].variable_type
        if ctx.children[3].getText() not in AliasType.table:
            identifier_type = self.getVariableType(identifier, type_id, ctx)
            if isinstance(self.type_table[type_id], ArrayType):
                identifier_type += "[" + self.getArraySize(ctx) + "]"
            elif isinstance(self.type_table[type_id], RecordType):
                self.visitChildren(ctx.children[3])
                identifier_type = ""
        else:
            identifier_type = ctx.children[3].getText()

        print(identifier)
        print("ctx size: ", len(ctx.children))
        print(ctx.children[2])

        post_declaration = ""
        if ctx.children[2].getText() == "is":
            post_declaration = " = " + ctx.children[3].getText()

        if len(ctx.children) > 4:
            post_declaration = " = " + ctx.children[5].getText()

        declaration = identifier_type + " " + identifier + post_declaration
        self.queue.append((declaration + ";").encode('ascii', 'ignore'))
        print(self.queue)
        return

    def getVariableType(self, identifier, type_id, ctx):
        if isinstance(self.type_table[type_id], PrimitiveType):
            print self.primitive_type_map[type_id]
            return self.primitive_type_map[type_id]
        elif isinstance(self.type_table[type_id], ArrayType):
            return self.getVariableType(identifier, self.type_table[type_id].nested_type_id, ctx)
        elif isinstance(self.type_table[type_id], RecordType):
            return
            return self.getVariableType(identifier, self.type_table[type_id].nested_type_id, ctx)

    def getArraySize(self, ctx):
        return self.expressionToString(ctx.getText().split('[')[1].split(']')[0])

    # Visit a parse tree produced by HelloParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx):
        type = self.type_table[AliasType.table[ctx.children[1].getText().encode('ascii', 'ignore')]]
        identifier = ctx.children[1].getText().encode('ascii', 'ignore')
        array_size = 0
        if isinstance(type, ArrayType):
            array_size = self.getArraySize(ctx)
        result = ""
        alias_name = ctx.children[3].children[0].children[0].children[4].getText().encode('ascii', 'ignore')

        if array_size != 0:
            array_size = "[" + str(array_size) + "]"
            if alias_name not in AliasType.table:
                alias_name = self.getVariableType(identifier,
                                                  AliasType.table[ctx.children[1].getText().encode('ascii', 'ignore')],
                                                  ctx.children[3])
            result = array_size
        else:
            if alias_name not in AliasType.table:
                alias_name = self.getVariableType(identifier,
                                                  AliasType.table[ctx.children[1].getText().encode('ascii', 'ignore')],
                                                  ctx.children[3])
        result = "typedef " + alias_name + " " + ctx.children[1].getText() + result
        self.type_def_queue.append(result.encode('ascii', 'ignore'))
        self.alias_list.append(identifier)
        print(self.type_def_queue)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#lang_type.
    def visitLang_type(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#primitiveType.
    def visitPrimitiveType(self, ctx):
        return self.visitChildren(ctx)

    #- Visit a parse tree produced by HelloParser#userType.
    def visitUserType(self, ctx):
        return self.visitChildren(ctx)

    #- Visit a parse tree produced by HelloParser#recordType.
    def visitRecordType(self, ctx):
        print(ctx.getText())
        print(ctx.children[0].getText())
        print(ctx.children[1].getText())
        print(ctx.children[2].getText())
        result = "struct " + ctx.children[0].getText()
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#arrayType.
    def visitArrayType(self, ctx):
        return self.visitChildren(ctx)

    #- Visit a parse tree produced by HelloParser#statement.
    def visitStatement(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#assignment.
    def visitAssignment(self, ctx):
        self.queue.append((ctx.children[0].getText() + " = " + ctx.children[2].getText() + ";").encode('ascii', 'ignore'))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#routineCall.
    def visitRoutineCall(self, ctx):
        self.queue.append(ctx.getText().encode('ascii', 'ignore') + ";")
        return self.visitChildren(ctx)

    #- Visit a parse tree produced by HelloParser#whileLoop.
    def visitWhileLoop(self, ctx):
        return self.visitChildren(ctx)

    #- Visit a parse tree produced by HelloParser#forLoop.
    def visitForLoop(self, ctx):
        print(ctx.getText())
        return self.visitChildren(ctx)

    #- Visit a parse tree produced by HelloParser#lang_range.
    def visitLang_range(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#ifStatement.
    def visitIfStatement(self, ctx):
        self.queue.append("if (" + self.expressionToString(self.visitExpression(ctx.children[1])) + ") {\n")
        self.visitBody(ctx.children[3])
        self.queue.append("}\n")
        return

    # Visit a parse tree produced by HelloParser#routineDeclaration.
    def visitRoutineDeclaration(self, ctx):
        self.current_scope = self.current_scope.child_scopes[ctx.children[1].getText()]
        routine_declaration = ""
        routine_declaration = "void " + ctx.children[1].getText() + " "
        routine_args = ctx.children[2].getText().replace('(', "").replace(')', "").split(",")
        args = ""
        for arg in routine_args:
            name = arg.split(":")[0]
            type = arg.split(":")[1]
            type_id = self.current_scope.scope[name.encode('ascii', 'ignore')].variable_type
            arg_type = self.type_table[type_id]
            if isinstance(arg_type, PrimitiveType):
                args += self.primitive_type_map[type_id] + " " + name + ", "
            else:
                args += self.c_type_map[arg_type] + " " + name + ", "
        if args is not "":
            args = args[:-2]
        routine_declaration += "(" + args + ") {\n"
        self.queue.append(routine_declaration.encode('ascii', 'ignore'))
        visit_children = self.visitChildren(ctx)
        self.current_scope = self.current_scope.parent_scope
        self.queue.append("}\n")
        print(self.queue)
        return visit_children

    # Visit a parse tree produced by HelloParser#parameters.
    def visitParameters(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx):
        return self.visitChildren(ctx)

    #- Visit a parse tree produced by HelloParser#body.
    def visitBody(self, ctx):
        return self.visitChildren(ctx)

    def expressionToString(self, expression):
        return expression.replace("and", " && ").replace("xor", " ^ ").replace("/=", " != ").replace("or", " || ")

    # Visit a parse tree produced by HelloParser#expression.
    def visitExpression(self, ctx):

        return ctx.getText().replace("and", "&&").replace("xor", "^").replace("/=", "!=").replace("or", "||").replace("=", "==").encode('ascii', 'ignore')
        # return self.visitChildren(ctx)

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
