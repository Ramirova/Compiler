from HelloVisitor import HelloVisitor
from SymbolTable import *
from TypeTable import *
import unicodedata

'''
The class that performs c code generation of a program tree. It uses instances of a 'Symbol table', 'TypeTable', 'AliasTable'
to get the types and make equivalent code in C.
'''


class CCodeGen(HelloVisitor):
    """
    Maps to get equivalent C type of the variable from type in I language
    """
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

    def __init__(self):
        """
        Initialization of the CCodeGen class and al its variables
        """
        self.current_scope = SymbolTable.root_table
        self.type_table = TypeTable.table
        self.alias_list = [] #List stores names of aliases of the types in language to covert them to "typedef" in C
        self.type_def_queue = [] #List which stores aliase declarations to types in language to covert them to "typedef" in C
        self.queue = [] #Main queue with variable and routines declarations
        self.current_queue = self.queue #Current queue variable to swtch between queue for nested structures
        self.record_state = False # Flag that currently we translate record in I to struct in C
        self.current_record = "" # VAriable contains the name of the record that we currently translate
        self.number_of_loops = 0
        self.routines = [] # List with the names of all routines declared
        self.record_values = "" # Variable stores the values in record that we currently translate
        self.scope_number = 0 #sequential number of subcscope in routine
        SymbolTable.reset_counters()

    def visitProgram(self, ctx):
        """
        Method starts visiting all notes from the root to make C file.
        :param ctx: current context - the root of the program
        :return: result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitSimpleDeclaration(self, ctx):
        """
        Visit a parse tree produced by HelloParser#simpleDeclaration.
        :param ctx: current context - the root of the simple declaration
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitVariableDeclaration(self, ctx):
        """
        Visit a parse tree produced by HelloParser#variableDeclaration.
        :param ctx: current context - the root of the variable declaration
        :return: the result of the visit all its children
        """
        identifier = ctx.Identifier().getText()
        identifier = unicodedata.normalize('NFKD', identifier).encode('ascii', 'ignore')
        if self.record_state:
            record_scope_id = self.current_scope.scope[self.current_record].variable_type
            type_id = self.type_table[record_scope_id].inner_declarations[identifier]
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
                self.current_queue.append(("typedef struct {\n").encode('ascii', 'ignore'))
                self.visitChildren(ctx.children[3])
                self.record_state = False
                self.current_record = ""
                self.current_queue.append(("} " + identifier + "_type" + ";").encode('ascii', 'ignore'))
                self.current_queue = self.queue
                self.current_queue.append(identifier + "_type " + identifier + "")
                if self.record_values != "":
                    self.current_queue.append((" = {" + self.record_values[:-2] + "}").encode('ascii', 'ignore'))
                self.current_queue.append(";\n")
                self.record_values = ""
                print(self.type_def_queue)
                print(self.queue)
                return
        else:
            identifier_type = ctx.children[3].getText()
        post_declaration = ""
        if ctx.children[2].getText() == "is":
            post_declaration = " = " + ctx.children[3].getText()
        if len(ctx.children) > 4:
            post_declaration = " = " + ctx.children[5].getText()
        if self.record_state:
            declaration = identifier_type + " " + identifier + "\n"
            if post_declaration != "":
                self.record_values += ctx.children[5].getText() + ", "
        else:
            declaration = identifier_type + " " + identifier + post_declaration
        self.current_queue.append((declaration + ";\n").encode('ascii', 'ignore'))
        print(self.current_queue)
        return

    def getVariableType(self, identifier, type_id, ctx):
        """
        Method return the type of the given variable using uts identifier and type ID from type table.
        :param identifier: the name of the variable
        :param type_id: id of the type of variable
        :param ctx: root of variable declaration
        :return: string with the name of the variable
        """
        if isinstance(self.type_table[type_id], PrimitiveType):
            print self.primitive_type_map[type_id]
            return self.primitive_type_map[type_id]
        elif isinstance(self.type_table[type_id], ArrayType):
            return self.getVariableType(identifier, self.type_table[type_id].nested_type_id, ctx)
        elif isinstance(self.type_table[type_id], RecordType):
            return

    def getArraySize(self, ctx):
        """
        Method gives the size of the array from the given context
        :param ctx: root of the current declaration
        :return: number which is the size of the array
        """
        return self.expressionToString(ctx.getText().split('[')[1].split(']')[0])

    def visitTypeDeclaration(self, ctx):
        """
        Visit a parse tree produced by HelloParser#typeDeclaration.
        :param ctx: current context - the root of the type declaration
        :return: the result of the visit all its children
        """
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

    def visitLang_type(self, ctx):
        """
        Visit a parse tree produced by HelloParser#lang_type.
        :param ctx: current context - the root of the lang type
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitPrimitiveType(self, ctx):
        """
        Visit a parse tree produced by HelloParser#primitiveType.
        :param ctx: current context - the root of the primitive type
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitUserType(self, ctx):
        """
        Visit a parse tree produced by HelloParser#userType.
        :param ctx: current context - the root of the user type
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitRecordType(self, ctx):
        """
        Visit a parse tree produced by HelloParser#recordType.
        :param ctx: current context - the root of the record type
        :return: the result of the visit all its children
        """
        print("End record declaration, go to variable declaration")
        self.record_state = True
        return self.visitChildren(ctx)

    def visitArrayType(self, ctx):
        """
        Visit a parse tree produced by HelloParser#arrayType.
        :param ctx: current context - the root of the array type
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitStatement(self, ctx):
        """
        Visit a parse tree produced by HelloParser#statement.
        :param ctx: current context - the root of the statement.
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitAssignment(self, ctx):
        """
        Visit a parse tree produced by HelloParser#assignment.
        :param ctx: current context - the root of the assignment
        :return: the result of the visit all its children
        """
        self.current_queue.append(
            (ctx.children[0].getText() + " = " + ctx.children[2].getText() + ";").encode('ascii', 'ignore'))
        return self.visitChildren(ctx)

    def visitRoutineCall(self, ctx):
        """
        Visit a parse tree produced by HelloParser#routineCall.
        :param ctx: current context - the root of the routine call
        :return: the result of the visit all its children
        """
        self.current_queue.append(ctx.getText().encode('ascii', 'ignore') + ";")
        return self.visitChildren(ctx)

    def visitWhileLoop(self, ctx):
        """
        Visit a parse tree produced by HelloParser#whileLoop.
        :param ctx: current context - the root of the while loop
        :return: the result of the visit all its children
        """
        self.current_scope = self.current_scope.child_scopes[self.current_scope.get_new_inner_scope_name()]
        self.current_queue.append("while (" + self.expressionToString(self.visitExpression(ctx.children[1]))
                                  + ")" + " {")
        self.visitChildren(ctx)
        self.current_scope = self.current_scope.parent_scope
        self.current_queue.append("}\n")
        return

    def visitForLoop(self, ctx):
        """
        Visit a parse tree produced by HelloParser#forLoop.
        :param ctx: current context - the root of the for loop
        :return: the result of the visit all its children
        """
        self.current_scope = self.current_scope.child_scopes[self.current_scope.get_new_inner_scope_name()]
        self.number_of_loops += 1
        self.current_queue.append(("int " + ctx.children[1].getText() +
                                   " = " + ctx.children[3].getText().split("..")[0]).encode('ascii', 'ignore'))
        iterator = ctx.children[1].getText()
        loop_range = ctx.children[3].getText().split("..")
        self.current_queue.append(("\nfor (int " + iterator + " = " + loop_range[0] + "; "
                                   + iterator + " < " + loop_range[1] + "; " + iterator + "++) {\n").encode('ascii',
                                                                                                            'ignore'))
        print(ctx.getText())
        self.visitChildren(ctx)
        self.current_scope = self.current_scope.parent_scope
        self.current_queue.append("}\n")
        return

    def visitLang_range(self, ctx):
        """
        Visit a parse tree produced by HelloParser#lang_range.
        :param ctx: current context - the root of the lang range
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitIfStatement(self, ctx):
        """
        Visit a parse tree produced by HelloParser#ifStatement.
        :param ctx: current context - the root of the if statement
        :return: the result of the visit all its children
        """
        self.current_queue.append("if (" + self.expressionToString(self.visitExpression(ctx.children[1])) + ") {\n")
        self.current_scope = self.current_scope.child_scopes[self.current_scope.get_new_inner_scope_name()]
        self.visitBody(ctx.children[3])
        self.current_scope = self.current_scope.parent_scope
        self.current_queue.append("}\n")
        return

    def visitRoutineDeclaration(self, ctx):
        """
        Visit a parse tree produced by HelloParser#routineDeclaration.
        :param ctx: current context - the root of the routine declaration.
        :return: the result of the visit all its children
        """
        self.current_scope = self.current_scope.child_scopes[ctx.children[1].getText()]
        self.routines.append(ctx.children[1].getText().encode('ascii', 'ignore'))

        routine_args = ctx.children[2].getText().replace('(', "").replace(')', "").split(",")
        args = ""
        if ":" in routine_args and len(routine_args) > 1:
            for arg in routine_args:
                name = arg.split(":")[0]
                type = arg.split(":")[1]
                type_id = self.current_scope.scope[name.encode('ascii', 'ignore')].variable_type
                arg_type = self.type_table[type_id]
                if isinstance(arg_type, PrimitiveType):
                    args += self.primitive_type_map[type_id] + " " + name + ", "
                else:
                    args += self.c_type_map[arg_type] + " " + name + ", "
        return_type = "void"

        if ":" in routine_args and len(routine_args) == 1:
            return_type = self.c_type_map[ctx.children[3].getText()]
        if args is not "":
            args = args[:-2]
        routine_declaration = return_type + " " + ctx.children[1].getText() + "(" + args + ")" + " {\n"
        self.current_queue.append(routine_declaration.encode('ascii', 'ignore'))
        visit_children = self.visitChildren(ctx)
        self.current_scope = self.current_scope.parent_scope
        return_index = -1
        for child in range(len(ctx.children)):
            if ctx.children[child].getText() == "return":
                return_index = child
        if len(ctx.children) >= 7 and return_index != -1:
            self.current_queue.append(("return " + ctx.children[return_index + 1].getText()).encode('ascii', 'ignore') + ";")
        self.current_queue.append("}\n")
        print(self.current_queue)
        return visit_children

    def visitParameters(self, ctx):
        """
        Visit a parse tree produced by HelloParser#parameters.
        :param ctx: current context - the root of the routine parameters
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitParameterDeclaration(self, ctx):
        """
        Visit a parse tree produced by HelloParser#parameterDeclaration.
        :param ctx: current context - the root of the parameter declaration
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitBody(self, ctx):
        """
        Visit a parse tree produced by HelloParser#body.
        :param ctx: current context - the root of the routine or loop body
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def expressionToString(self, expression):
        """
        Method which vonvers I language expression to C lang expression
        :param expression: I language expression
        :return: expression in C
        """
        return expression.replace("and", " && ").replace("xor", " ^ ").replace("/=", " != ").replace("or", " || ")

    def visitExpression(self, ctx):
        """
        Visit a parse tree produced by HelloParser#expression.
        :param ctx: current context - the root of the expression
        :return: string with expression in C
        """
        return ctx.getText().replace("and", "&&").replace("xor", "^").replace("/=", "!=").replace("or", "||").replace(
            "=", "==").encode('ascii', 'ignore')

    def visitRelation(self, ctx):
        """
        Visit a parse tree produced by HelloParser#relation.
        :param ctx: current context - the root of the relation
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitSimple(self, ctx):
        """
        Visit a parse tree produced by HelloParser#simple.
        :param ctx: current context - the root of the simple
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitFactor(self, ctx):
        """
        Visit a parse tree produced by HelloParser#factor.
        :param ctx: current context - the root of the factor
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)


    def visitSummand(self, ctx):
        """
        Visit a parse tree produced by HelloParser#summand.
        :param ctx: current context - the root of the summand
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitPrimary(self, ctx):
        """
        Visit a parse tree produced by HelloParser#primary.
        :param ctx: current context - the root of the primary
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitModifiablePrimary(self, ctx):
        """
        Visit a parse tree produced by HelloParser#modifiablePrimary.
        :param ctx: current context - the root of the modifiable primary
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)

    def visitEos(self, ctx):
        """
        Visit a parse tree produced by HelloParser#eos.
        :param ctx: current context - the root of the Eos
        :return: the result of the visit all its children
        """
        return self.visitChildren(ctx)
