from HelloVisitor import HelloVisitor
from SymbolTable import SymbolTable
from HelloParser import HelloParser
from TypeTable import *
import unicodedata


class SymbolTableGenerator(HelloVisitor):
    current_symbol_table = SymbolTable(parent=None)
    type_table = TypeTable
    type_table.table[1] = PrimitiveType()
    type_table.table[2] = PrimitiveType()
    type_table.table[3] = PrimitiveType()

    def visitProgram(self, ctx):
        a = self.visitChildren(ctx)
        return a

    # Visit a parse tree produced by HelloParser#simpleDeclaration.
    def visitSimpleDeclaration(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx):
        identifier = ctx.Identifier().getText()
        identifier = unicodedata.normalize('NFKD', identifier).encode('ascii', 'ignore')
        lang_type = self.visitLang_type(ctx)
        if self.current_symbol_table.is_defined_in_scope(identifier):
            raise Exception('Variable {} is already defined'.format(identifier))
        if lang_type is None:
            expression = ctx.expression()
            expr_children = expression.children
            if len(expr_children) > 1:
                lang_type = PrimitiveType.types['boolean']
            elif expr_children[0].children > 1:
                lang_type = PrimitiveType.types['boolean']
        self.current_symbol_table.add(identifier, lang_type)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx):
        id = ctx.Identifier().getText()
        id = unicodedata.normalize('NFKD', id).encode('ascii', 'ignore')
        current_type = self.visitLang_type(ctx)

        AliasType.table[id] = current_type

        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#lang_type.
    def visitLang_type(self, ctx):
        children = ctx.children
        if len(children) > 3 and hasattr(ctx.children[3], 'Identifier') and ctx.children[3].Identifier() is not None:
            id = ctx.children[3].Identifier().getText()
            id = unicodedata.normalize('NFKD', id).encode('ascii', 'ignore')
            return AliasType.table[id]
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#primitiveType.
    def visitPrimitiveType(self, ctx):
        c = ctx.children[0].getText()
        c = unicodedata.normalize('NFKD', c).encode('ascii', 'ignore')
        id = PrimitiveType.types[c]
        return id

    # Visit a parse tree produced by HelloParser#userType.
    def visitUserType(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#recordType.
    def visitRecordType(self, ctx):
        self.current_symbol_table = self.current_symbol_table.create_child_scope('current_record')
        children = ctx.children
        record_variables = {}
        for c in children:
            if type(c) == HelloParser.VariableDeclarationContext:
                var_name = unicodedata.normalize('NFKD', c.children[1].getText()).encode('ascii', 'ignore')
                var_type = self.visitLang_type(c)
                record_variables[var_name] = var_type
        recur = self.visitChildren(ctx)
        new_type = RecordType(record_variables)
        self.current_symbol_table = self.current_symbol_table.parent_scope
        self.current_symbol_table.remove_child_scope('current_record')
        return new_type.get_id()

    # Visit a parse tree produced by HelloParser#arrayType.
    def visitArrayType(self, ctx):
        nested_type = self.visitChildren(ctx)
        new_type = ArrayType(nested_type)
        return new_type.get_id()

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
        return_type = self.current_symbol_table.get_routine_info(routine_name).return_type
        self.visitChildren(ctx)
        return return_type

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
        if ctx.parameters() is not None:
            parameters_context = ctx.parameters().children
            declarations = []
            for i in range(len(parameters_context)):
                if i % 2 == 1:
                    declarations.append(parameters_context[i])
            parameters = {}
            for d in declarations:
                id, t = self.visitParameterDeclaration(d)
                parameters[id] = t
        else:
            parameters = None
        if ctx.lang_type() is not None:
            return_type = self.visitLang_type(ctx.lang_type())
        else:
            return_type = None
        if self.current_symbol_table.routine_defined_in_scope(identifier):
            raise Exception('Routine {} is already defined'.format(identifier))
        self.current_symbol_table.add_routine(identifier, parameters, return_type)
        self.current_symbol_table = self.current_symbol_table.create_child_scope(identifier)
        peremennaya = self.visitChildren(ctx)
        self.current_symbol_table = self.current_symbol_table.parent_scope
        return peremennaya

    # Visit a parse tree produced by HelloParser#parameters.
    def visitParameters(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx):
        id = ctx.children[0].getText()
        id = unicodedata.normalize('NFKD', id).encode('ascii', 'ignore')
        lang_type = self.visitLang_type(ctx)
        if self.current_symbol_table.is_defined_in_current_scope(id):
            raise Exception('Parameter with name {} is already defined'.format(id))
        self.current_symbol_table.add(id, lang_type)
        self.visitChildren(ctx)
        return id, lang_type

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
        factor_type = self.visitSummand(children[0])
        if len(children) > 1:
            factor_type = TypeUtils.deduce_type(self.visitSummand(children[0]), self.visitSummand(children[2]))
        return factor_type

    # Visit a parse tree produced by HelloParser#summand.
    def visitSummand(self, ctx):
        c = self.visitChildren(ctx)
        return c

    # Visit a parse tree produced by HelloParser#primary.
    def visitPrimary(self, ctx):
        primitives = [1, 2, 3]
        child_type = self.visitChildren(ctx)
        children = ctx.children
        type_id = None

        int_lit = ctx.IntegerLiteral()
        real_lit = ctx.RealLiteral()
        routine_call = ctx.routineCall()

        if routine_call is not None:  # if primary is routine call
            type_id = self.visitRoutineCall(routine_call)
        elif int_lit is not None:  # if primary is integer
            type_id = PrimitiveType.integer
        elif real_lit is not None:  # if primary is real
            type_id = PrimitiveType.real
        elif unicodedata.normalize('NFKD', children[0].getText()).encode('ascii',
                                                                         'ignore') == 'true' or unicodedata.normalize(
            'NFKD', children[0].getText()).encode('ascii', 'ignore') == 'false':  # if primary is boolean
            type_id = PrimitiveType.boolean
        else:  # if primary is modifiable primary
            type_id = child_type
        return type_id

    # Visit a parse tree produced by HelloParser#modifiablePrimary.
    def visitModifiablePrimary(self, ctx):
        self.visitChildren(ctx)
        children = ctx.children

        identifier = None
        array_identifier = None
        function_calls = []

        if len(children) == 1:
            identifier = children[0].getText()
            identifier = unicodedata.normalize('NFKD', identifier).encode('ascii', 'ignore')
            if not self.current_symbol_table.is_defined_in_scope(identifier):
                raise Exception('Variable {} is not defined'.format(identifier))
            return self.current_symbol_table.get_variable_info(identifier).variable_type
        elif type(children[2]) is HelloParser.ExpressionContext:
            array_identifier = children[0].getText()
            array_identifier = unicodedata.normalize('NFKD', array_identifier).encode('ascii', 'ignore')
            if not self.current_symbol_table.is_defined_in_scope(array_identifier):
                raise Exception('Array with name {} is not defined'.format(array_identifier))
            return self.current_symbol_table.get_variable_info(array_identifier).variable_type
        else:
            for i in range(len(children)):
                if i % 2 == 0:
                    id = children[i].getText()
                    id = unicodedata.normalize('NFKD', id).encode('ascii', 'ignore')
                    # TODO check validity of record fields
                    # check that the first identifier is a declared variable with type record
                    if i == 0 and not self.current_symbol_table.is_defined_in_scope(id):
                        raise Exception('Record with name {} is not defined'.format(id))
                    function_calls.append(id)

            type_id = self.current_symbol_table.get_variable_info(function_calls[0]).variable_type
            current_type = self.type_table.table[type_id]
            for i in range(len(function_calls) - 1):
                if function_calls[i + 1] not in current_type.inner_declarations.keys():
                    raise Exception(
                        "Record {} doesn't have a field {}".format(function_calls[i], function_calls[i + 1]))
                type_id = current_type.inner_declarations[function_calls[i + 1]]
                current_type = self.type_table.table[type_id]
            return type_id

    # Visit a parse tree produced by HelloParser#eos.
    def visitEos(self, ctx):
        return self.visitChildren(ctx)
