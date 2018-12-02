from HelloVisitor import HelloVisitor
from SymbolTable import *
from TypeTable import *
import unicodedata


class CCodeGen(HelloVisitor):

    c_type_map = {
            "integer" : "int",
            "real": "double",
            "boolean": "bool",
        }

    primitive_type_map = {
        1: "int",
        0: "double",
        2: "bool"
    }

    def __init__(self, args):
        # self.code_file = open("c_code.c", "w+")
        # self.code_file.write("#include <stdio.h>\n")
        # self.code_file.write("int main()\n")
        # self.code_file.write("{\n")\
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
        lang_type = self.visitLang_type(ctx)
        SymbolTable.root_table
        type_id = self.current_scope.scope[identifier].variable_type
        if ctx.children[3].getText() not in AliasType.table:
            identifier_type = self.getVariableType(identifier, type_id, ctx)
            if isinstance(self.type_table[type_id], ArrayType):
                identifier_type += "[" + self.getArraySize(ctx) + "]"
            elif isinstance(self.type_table[type_id], RecordType):
                identifier_type = self.getVariableType(identifier, type_id, ctx) + ""
        else:
            identifier_type = ctx.children[3].getText()

        declaration = identifier_type + " " + identifier
        self.queue.append((declaration + ";").encode('ascii', 'ignore'))
        print(self.queue)
        return

    def getVariableType(self, identifier, type_id, ctx):
        print(identifier)
        # if identifier in self.alias_list:
        #     return identifier

        if isinstance(self.type_table[type_id], PrimitiveType):
            return self.primitive_type_map[type_id]
        elif isinstance(self.type_table[type_id], ArrayType):
            return self.getVariableType(identifier, self.type_table[type_id].nested_type_id, ctx)
        elif isinstance(self.type_table[type_id], RecordType):
            return self.getVariableType(identifier, self.type_table[type_id].nested_type_id, ctx)

    def getArraySize(self, ctx):
        # print("Privet")
        # print(ctx.children[3].getText())
        print(ctx.children[0])

        return ctx.getText().split('[')[1].split(']')[0]
        # return ctx.children[3].children[0].children[0].children[2].getText()

    # Visit a parse tree produced by HelloParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx):
        # print(AliasType.table)
        # print(AliasType.table[ctx.children[1].getText()])
        # print(self.current_scope.scope)
        # print(self.type_table[AliasType.table[ctx.children[1].getText().encode('ascii', 'ignore')]])
        type = self.type_table[AliasType.table[ctx.children[1].getText().encode('ascii', 'ignore')]]
        identifier = ctx.children[1].getText().encode('ascii', 'ignore')
        print("id", identifier)
        # print("Type: ", type)
        array_size = 0
        result = ""
        if isinstance(type, ArrayType):
            array_size = self.getArraySize(ctx)
        alias_type = ""
        if array_size != 0:
            if identifier in self.alias_list:
                alias_type = identifier
            else:
                alias_type = self.getVariableType(identifier,
                    AliasType.table[ctx.children[1].getText().encode('ascii', 'ignore')], ctx.children[3]) + "[" + array_size + "] " + \
                     ctx.children[1].getText()
            result = "typedef " + alias_type
        else:
            if identifier in AliasType.table:
                alias_type = identifier
            else:
                alias_type = self.getVariableType(identifier,
                    AliasType.table[ctx.children[1].getText().encode('ascii', 'ignore')], ctx.children[3]) + \
                     ctx.children[1].getText()
            result = "typedef " + alias_type


        print(array_size)
        # result = "typedef " + self.getVariableType(AliasType.table[ctx.children[1].getText().encode('ascii', 'ignore')], ctx.children[3]) + " " + ctx.children[1].getText()
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
            args += self.c_type_map[arg_type] + " " + name + ", "
        if args is not "":
            args = args[:-2]
        routine_declaration += "(" + args + ") {\n"
        self.queue.append(routine_declaration)
        print(routine_declaration)
        visit_children = self.visitChildren(ctx)
        self.current_scope = self.current_scope.parent
        self.queue.append("}\n")
        return visit_children

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
        return ctx.getText().replace("and", "&&").replace("xor", "^").replace("/=", "!=").replace("or", "||")
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
        # children = ctx.children
        # print(children[0].getText())
        # print(children[1].getText())
        # print(children[2].getText())
        # print(children[3].getText())
        # function_calls = []
        #
        # if len(children) == 1:
        #     identifier = children[0].getText()
        #     identifier = unicodedata.normalize('NFKD', identifier).encode('ascii', 'ignore')
        #     if not self.current_symbol_table.is_defined_in_scope(identifier):
        #         raise Exception('Variable {} is not defined'.format(identifier))
        # elif type(children[2]) is HelloParser.ExpressionContext:
        #     array_identifier = children[0].getText()
        #     array_identifier = unicodedata.normalize('NFKD', array_identifier).encode('ascii', 'ignore')
        #     if not self.current_symbol_table.is_defined_in_scope(array_identifier):
        #         raise Exception('Array with name {} is not defined'.format(array_identifier))
        # else:
        #     for i in range(len(children)):
        #         if i % 2 == 0:
        #             id = children[i].getText()
        #             id = unicodedata.normalize('NFKD', id).encode('ascii', 'ignore')
        #             # TODO check validity of record fields
        #             # check that the first identifier is a declared variable with type record
        #             if i == 0 and not self.current_symbol_table.is_defined_in_scope(id):
        #                 raise Exception('Record with name {} is not defined'.format(id))
        #             function_calls.append(id)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#eos.
    def visitEos(self, ctx):
        return self.visitChildren(ctx)