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
        self.current_queue = self.queue
        self.record_state = False
        self.current_record = ""
        self.number_of_loops = 0

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
        if self.record_state:
            record_scope_id = self.current_scope.scope[self.current_record].variable_type
            type_id = self.type_table[record_scope_id].inner_declarations[identifier]
            print(type_id)
            # type_id = self.type_table[]
        else:
            type_id = self.current_scope.scope[identifier].variable_type
        if ctx.children[3].getText() not in AliasType.table:
            identifier_type = self.getVariableType(identifier, type_id, ctx)
            if isinstance(self.type_table[type_id], ArrayType):
                identifier_type += "[" + self.getArraySize(ctx) + "]"
            elif isinstance(self.type_table[type_id], RecordType):
                print("qq", ctx.children[3].children[0].children[0].children[1].getText())
                self.record_state = True
                self.current_queue = self.type_def_queue
                self.current_record = identifier
                self.current_record = identifier
                self.current_queue.append(("typedef struct " + identifier + "_type {\n").encode('ascii', 'ignore'))
                self.visitChildren(ctx.children[3])
                self.record_state = False
                self.current_record = ""
                self.current_queue.append(("};").encode('ascii', 'ignore'))
                self.current_queue = self.queue
                self.current_queue.append(identifier + "_type " + identifier + ";")
                print(self.type_def_queue)
                print(self.queue)
                return
                # identifier_type = id
        else:
            identifier_type = ctx.children[3].getText()

        # print(identifier)
        # print("ctx size: ", len(ctx.children))
        # print(ctx.children[2])

        post_declaration = ""
        if ctx.children[2].getText() == "is":
            post_declaration = " = " + ctx.children[3].getText()

        if len(ctx.children) > 4:
            post_declaration = " = " + ctx.children[5].getText()

        declaration = identifier_type + " " + identifier + post_declaration
        self.current_queue.append((declaration + ";").encode('ascii', 'ignore'))
        print(self.current_queue)
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

    # Visit a parse tree produced by HelloParser#userType.
    def visitUserType(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#recordType.
    def visitRecordType(self, ctx):
        # print(ctx.getText())
        # print(ctx.children[0].getText())
        # print(ctx.children[1].getText())
        # print(ctx.children[2].getText())
        print("End record declaration, go to variable declaration")
        # self.queue.append(("struct " + ctx.children[0].getText()).encode('ascii', 'ignore'))
        self.record_state = True
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#arrayType.
    def visitArrayType(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#statement.
    def visitStatement(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#assignment.
    def visitAssignment(self, ctx):
        self.current_queue.append((ctx.children[0].getText() + " = " + ctx.children[2].getText() + ";").encode('ascii', 'ignore'))
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#routineCall.
    def visitRoutineCall(self, ctx):
        self.current_queue.append(ctx.getText().encode('ascii', 'ignore') + ";")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#whileLoop.
    def visitWhileLoop(self, ctx):
        self.current_queue.append("while (" + self.expressionToString(self.visitExpression(ctx.children[1]))
                                  + ")" + " {")
        self.visitChildren(ctx)
        self.current_queue.append("}\n")
        return

    # Visit a parse tree produced by HelloParser#forLoop.
    def visitForLoop(self, ctx):
        self.number_of_loops += 1
        self.current_queue.append(("int " + ctx.children[1].getText() +
                                   " = " + ctx.children[3].getText().split("..")[0]).encode('ascii', 'ignore'))
        iterator = ctx.children[1].getText()
        loop_range = ctx.children[3].getText().split("..")
        self.current_queue.append(("for (int " + iterator + " = " + loop_range[0] + "; "
                                   + iterator + " < " + loop_range[1] + "; " + iterator + "++) {\n").encode('ascii', 'ignore'))
        print(ctx.getText())
        self.visitChildren(ctx)
        self.current_queue.append("}\n")
        return

    # Visit a parse tree produced by HelloParser#lang_range.
    def visitLang_range(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#ifStatement.
    def visitIfStatement(self, ctx):
        self.current_queue.append("if (" + self.expressionToString(self.visitExpression(ctx.children[1])) + ") {\n")
        self.visitBody(ctx.children[3])
        self.current_queue.append("}\n")
        return

    # Visit a parse tree produced by HelloParser#routineDeclaration.
    def visitRoutineDeclaration(self, ctx):
        self.current_scope = self.current_scope.child_scopes[ctx.children[1].getText()]
        routine_declaration = "void " + ctx.children[1].getText()
        routine_args = ctx.children[2].getText().replace('(', "").replace(')', "").split(",")
        args = ""
        if ":" in routine_args > 0:
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
        self.current_queue.append(routine_declaration.encode('ascii', 'ignore'))
        visit_children = self.visitChildren(ctx)
        self.current_scope = self.current_scope.parent_scope
        self.current_queue.append("}\n")
        print(self.current_queue)
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
