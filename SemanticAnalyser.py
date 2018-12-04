from lexical_and_syntax_analysis.HelloVisitor import HelloVisitor
from SymbolTable import SymbolTable
from lexical_and_syntax_analysis.HelloParser import HelloParser
from TypeTable import *
import unicodedata

"""
The class that performs semantic analysis of a program tree. Uses instances of a 'Symbol table' to define scopes of 
internal structures (variables, routines, loops and if-statements), and a 'Type table' to keep track of types
- primitive as well as user-defined. 

"""


class SemanticAnalyser(HelloVisitor):
    """Global variables"""
    current_symbol_table = SymbolTable(parent=None)
    type_table = TypeTable
    type_table.table[1] = PrimitiveType()
    type_table.table[2] = PrimitiveType()
    type_table.table[3] = PrimitiveType()

    @staticmethod
    def unicode_to_str(unicode_str):
        """
        Function to convert unicode string to ascii string
        :param unicode_str: sring in format u'__any_string__'
        :return: ascii string
        """
        return unicodedata.normalize('NFKD', unicode_str).encode('ascii', 'ignore')

    def visitProgram(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#simpleDeclaration.
    def visitSimpleDeclaration(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#variableDeclaration.
    def visitVariableDeclaration(self, ctx):
        #  array with all children of a current context
        children = ctx.children

        #  get the context of children
        identifier = self.unicode_to_str(ctx.Identifier().getText())
        lang_type = self.visitChildren(ctx)
        expression = ctx.expression()

        #  if type is specified deduce type
        if len(children) > 4:
            lang_type = self.visitLang_type(children[3])
        final_type = lang_type

        #  check if the variable was already defined in the current scope
        if self.current_symbol_table.is_defined_in_current_scope(identifier):
            raise Exception('Variable {} is already defined'.format(identifier))

        #  deduce type from expression if no explicit type was specified
        if lang_type is None:  # 'var' Identifier 'is' expression
            final_type = self.visitExpression(expression)
        #  check if explicit type definition corresponds to the expression type
        elif lang_type is not None and expression is not None:  # 'var' Identifier ':' lang_type 'is' expression
            expression_type = self.visitExpression(expression)
            if lang_type != expression_type:
                raise Exception('Incompatible types in variable declaration {} '.format(identifier))

        #  add variable to the symbol table
        self.current_symbol_table.add_variable(identifier, final_type)

    # Visit a parse tree produced by HelloParser#typeDeclaration.
    def visitTypeDeclaration(self, ctx):
        #  get the context of children
        identifier = self.unicode_to_str(ctx.Identifier().getText())
        current_type = self.visitLang_type(ctx)

        #  add alias for the type to the Type table
        AliasType.table[identifier] = current_type

    # Visit a parse tree produced by HelloParser#lang_type.
    def visitLang_type(self, ctx):
        #  array with all children of a current context
        children = ctx.children

        #  if type declaration is an alias to an existing alias
        if len(children) > 3 and hasattr(ctx.children[3], 'Identifier') and ctx.children[3].Identifier() is not None:
            identifier = self.unicode_to_str(ctx.children[3].Identifier().getText())
            return AliasType.table[identifier]

        #  integrating the Universe
        if len(children) == 1 and self.unicode_to_str(children[0].getText()) in AliasType.table.keys():
            return AliasType.table[children[0].getText()]
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#primitiveType.
    def visitPrimitiveType(self, ctx):
        #  getting a code of a type from the Type table
        p_text = self.unicode_to_str(ctx.children[0].getText())
        identifier = PrimitiveType.types[p_text]
        return identifier

    # Visit a parse tree produced by HelloParser#userType.
    def visitUserType(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#recordType.
    def visitRecordType(self, ctx):
        #  creating a new scope for the record in order to define new types
        self.current_symbol_table = self.current_symbol_table.create_child_scope('current_record')

        #  array with all children of a current context
        children = ctx.children

        #  creating a dictionary with variables defined in the record
        record_variables = {}
        for c in children:
            if type(c) == HelloParser.VariableDeclarationContext:
                var_name = self.unicode_to_str(c.children[1].getText())
                var_type = self.visitLang_type(c)
                record_variables[var_name] = var_type

        #  define this record as a new type
        new_type = RecordType(record_variables)
        self.current_symbol_table = self.current_symbol_table.parent_scope

        #  remove the scope because records don't have a scope,
        #  we just needed it to add tew variables and define a new type
        self.current_symbol_table.remove_child_scope('current_record')
        return new_type.get_id()

    # Visit a parse tree produced by HelloParser#arrayType.
    def visitArrayType(self, ctx):
        #  get the type of array elements
        nested_type = self.visitChildren(ctx)

        #  create a new type of array
        new_type = ArrayType(nested_type)

        #  check type in case the size of the array is defined with expression
        expression = ctx.children[2]
        if self.visitExpression(expression) != PrimitiveType.integer:
            raise Exception('Array size can only be integer')
        return new_type.get_id()

    # Visit a parse tree produced by HelloParser#statement.
    def visitStatement(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#assignment.
    def visitAssignment(self, ctx):
        #  getting assignment contexts and their types
        lhs = ctx.modifiablePrimary()
        rhs = ctx.expression()
        lhs_type = self.visitModifiablePrimary(lhs)
        rhs_type = self.visitExpression(rhs)

        #  checking assignment types compatibility
        if TypeTable.get_type_name(lhs_type) == 'ArrayType':
            #  if trying to assign incompatible type to an array element
            if TypeTable.table[lhs_type].nested_type_id != rhs_type:
                raise Exception('Cannot assign {} to array with elements of type {}'.format(rhs_type, lhs_type))
            else:
                return self.visitChildren(ctx)
        #  check for assignment of real to boolean
        elif not TypeUtils.are_compatible_for_assignment(lhs_type, rhs_type):
            raise Exception(
                'Types {} and {} are not compatible for assignment'.format(TypeTable.get_type_name(lhs_type),
                                                                           TypeTable.get_type_name(rhs_type)))

    # Visit a parse tree produced by HelloParser#routineCall.
    def visitRoutineCall(self, ctx):
        #  getting context children, routine name and return type
        children = ctx.children
        routine_name = self.unicode_to_str(ctx.Identifier().getText())
        return_type = self.current_symbol_table.get_routine_info(routine_name).return_type
        routine_parameters = self.current_symbol_table.get_routine_info(routine_name).parameters

        #  check if routine was defined
        if not self.current_symbol_table.routine_defined_in_scope(routine_name):
            raise Exception('Routine {} is not defined'.format(routine_name))

        #  constructing routine call argument list
        arguments = []
        for c in children:
            if type(c) == HelloParser.ExpressionContext:
                arguments.append(c)

        #  check number of arguments compatibility
        if len(routine_parameters) != len(arguments):
            raise Exception("Wrong number of arguments in routine call {}".format(routine_name))

        #  check argument types and parameter types compatibility
        for p, a in zip(routine_parameters, arguments):
            argument_type = self.visitExpression(a)
            if not TypeUtils.are_compatible_for_assignment(p, argument_type):
                raise Exception(
                    'Parameter of type {} and argument of type {} are not compatible in {} routine call'.format(
                        TypeTable.get_type_name(p),
                        TypeTable.get_type_name(argument_type), routine_name))
        return return_type

    # Visit a parse tree produced by HelloParser#whileLoop.
    def visitWhileLoop(self, ctx):
        #  creating new scope for while loop
        self.current_symbol_table = self.current_symbol_table.create_child_scope(
            self.current_symbol_table.get_new_inner_scope_name())

        #  visiting while loop context children
        self.visitChildren(ctx)

        #  returning to higher scope
        self.current_symbol_table = self.current_symbol_table.parent_scope

    # Visit a parse tree produced by HelloParser#forLoop.
    def visitForLoop(self, ctx):
        #  creating new scope for 'for' loop
        self.current_symbol_table = self.current_symbol_table.create_child_scope(
            self.current_symbol_table.get_new_inner_scope_name())

        #  adding loop iteration variable to loops scope
        identifier = self.unicode_to_str(ctx.Identifier().getText())
        self.current_symbol_table.add_variable(identifier, PrimitiveType.integer)

        #  visiting for loop context children
        self.visitChildren(ctx)

        #  returning to higher scope
        self.current_symbol_table = self.current_symbol_table.parent_scope

    # Visit a parse tree produced by HelloParser#lang_range.
    def visitLang_range(self, ctx):
        #  getting context children, start and end of the range and theit types
        children = ctx.children
        start_range = children[0]
        end_range = children[2]
        start_type = self.visitExpression(start_range)
        end_type = self.visitExpression(end_range)

        #  check range boundaries to be integers
        if start_type != PrimitiveType.integer or end_type != PrimitiveType.integer:
            raise Exception('Range boundaries are not integer numbers')

    # Visit a parse tree produced by HelloParser#ifStatement.
    def visitIfStatement(self, ctx):
        #  getting context children
        children = ctx.children
        expression = children[1]

        #   creating new scope for if statement
        self.current_symbol_table = self.current_symbol_table.create_child_scope(
            self.current_symbol_table.get_new_inner_scope_name())

        #  check if condition to be boolean
        if self.visitExpression(expression) != PrimitiveType.boolean:
            raise Exception("Condition of if statement is not boolean")

        #  visit if body
        self.visitBody(children[3])

        #  returning to higher scope
        self.current_symbol_table = self.current_symbol_table.parent_scope

        #  check else case
        if len(children) > 5:
            #  creating new scope for else statement
            self.current_symbol_table = self.current_symbol_table.create_child_scope(
                self.current_symbol_table.get_new_inner_scope_name())

            #  visit else body
            self.visitBody(children[5])

            #  returning to higher scope
            self.current_symbol_table = self.current_symbol_table.parent_scope

    # Visit a parse tree produced by HelloParser#routineDeclaration.
    def visitRoutineDeclaration(self, ctx):
        # getting context children
        identifier = self.unicode_to_str(ctx.Identifier().getText())
        routine_parameters = ctx.parameters()
        routine_return_type = ctx.lang_type()
        return_expression = ctx.expression()
        body = ctx.body()

        #  check if routine with this name already exists
        if self.current_symbol_table.routine_defined_in_scope(identifier):
            raise Exception('Routine {} is already defined'.format(identifier))

        #  create a new scope for routine
        self.current_symbol_table = self.current_symbol_table.create_child_scope(identifier)

        #  check routine parameters declaration and construct a list woth those parameters
        if routine_parameters is not None:
            parameters_children = ctx.parameters().children
            declarations = []
            for i in range(len(parameters_children)):
                if i % 2 == 1:
                    declarations.append(parameters_children[i])
            parameters_list = []
            for d in declarations:
                _, t = self.visitParameterDeclaration(d)
                parameters_list.append(t)
        else:
            parameters_list = None

        #  check return type ans return statement consistency
        if routine_return_type is not None:
            return_type = self.visitLang_type(routine_return_type)
            if return_expression is None:
                raise Exception("Routine must have a return statement")
        else:
            return_type = None
            if return_expression is not None:
                raise Exception("Routine has no return type")

        #  add routine to the scope
        self.current_symbol_table.parent_scope.add_routine(identifier, parameters_list, return_type)

        #  visit body
        if body is not None:
            self.visitBody(body)

        #  check expression in return statement to be of routines return type
        if return_expression is not None:
            expr_type = self.visitExpression(return_expression)
            if return_type != expr_type:
                raise Exception("Return type must be {}".format(TypeTable.get_type_name(return_type)))

        #  returning to higher scope
        self.current_symbol_table = self.current_symbol_table.parent_scope

    # Visit a parse tree produced by HelloParser#parameters.
    def visitParameters(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#parameterDeclaration.
    def visitParameterDeclaration(self, ctx):
        #  getting context children
        identifier = self.unicode_to_str(ctx.children[0].getText())
        lang_type = self.visitLang_type(ctx)

        #  chech is parameter with this name is already defined
        if self.current_symbol_table.is_defined_in_current_scope(identifier):
            raise Exception('Parameter with name {} is already defined'.format(identifier))

        #  add variable to current scope
        self.current_symbol_table.add_variable(identifier, lang_type)
        return identifier, lang_type

    # Visit a parse tree produced by HelloParser#body.
    def visitBody(self, ctx):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by HelloParser#expression.
    def visitExpression(self, ctx):
        #  getting context children
        children = ctx.children

        #  if one child get and return type
        if len(children) <= 1:
            expression_type = self.visitRelation(children[0])
            return expression_type

        #  if both relations are present get their types
        left_type = self.visitRelation(children[0])
        right_type = self.visitRelation(children[2])

        #  check if both are boolean
        if left_type != PrimitiveType.boolean or right_type != PrimitiveType.boolean:
            raise Exception('Incompatible types {} and {} in expression, can be applied to boolean only'.format(
                TypeTable.get_type_name(left_type), TypeTable.get_type_name(right_type)))

        #  return expression type
        expression_type = PrimitiveType.boolean
        return expression_type

    # Visit a parse tree produced by HelloParser#relation.
    def visitRelation(self, ctx):
        #  getting context children
        children = ctx.children

        #  if one child get and return type
        if len(children) <= 1:
            return self.visitSimple(children[0])

        #  if both relations are present check their type compatibility
        left_type = self.visitSimple(children[0])
        right_type = self.visitSimple(children[2])
        TypeUtils.deduce_type_comparable(left_type, right_type)
        return PrimitiveType.boolean

    # Visit a parse tree produced by HelloParser#simple.
    def visitSimple(self, ctx):
        #  getting context children
        children = ctx.children
        simple_type = self.visitFactor(children[0])

        #  if one child get and return type
        if len(children) <= 1:
            return simple_type

        #  get operator
        operator = children[1]

        #  if both relations are present check their type compatibility according to the operator
        if operator is not None:
            left = children[0]
            right = children[2]
            operator_text = self.unicode_to_str(operator.getText())
            if operator_text == '*':
                simple_type = TypeUtils.deduce_type(self.visitFactor(left), self.visitFactor(right))
            elif operator_text == '/':
                simple_type = TypeUtils.deduce_type_division(self.visitFactor(left), self.visitFactor(right))
            elif operator_text == '%':
                simple_type = TypeUtils.deduce_type_module(self.visitFactor(left), self.visitFactor(right))
        return simple_type

    # Visit a parse tree produced by HelloParser#factor.
    def visitFactor(self, ctx):
        #  getting context children
        children = ctx.children
        factor_type = self.visitSummand(children[0])

        #  if one child get and return type
        if len(children) <= 1:
            return factor_type

        #  if both relations are present check their type compatibility
        if len(children) > 1:
            left = children[0]
            right = children[2]
            factor_type = TypeUtils.deduce_type(self.visitSummand(left), self.visitSummand(right))
        return factor_type

    # Visit a parse tree produced by HelloParser#summand.
    def visitSummand(self, ctx):
        #  getting context children
        children = ctx.children
        summand_type = self.visitChildren(ctx)

        #  if summand is an expression
        if len(children) == 3:
            return self.visitExpression(children[1])

        return summand_type

    # Visit a parse tree produced by HelloParser#primary.
    def visitPrimary(self, ctx):
        #  getting context children
        children = ctx.children
        child_type = self.visitChildren(ctx)
        int_lit = ctx.IntegerLiteral()
        real_lit = ctx.RealLiteral()
        routine_call = ctx.routineCall()

        #  deduce primary type
        if routine_call is not None:  # if primary is routine call
            type_id = self.visitRoutineCall(routine_call)
        elif int_lit is not None:  # if primary is integer
            type_id = PrimitiveType.integer
        elif real_lit is not None:  # if primary is real
            type_id = PrimitiveType.real
        elif self.unicode_to_str(children[0].getText()) == 'true' or self.unicode_to_str(
                children[0].getText()) == 'false':  # if primary is boolean
            type_id = PrimitiveType.boolean
        else:  # if primary is modifiable primary
            type_id = child_type
        return type_id

    # Visit a parse tree produced by HelloParser#modifiablePrimary.
    def visitModifiablePrimary(self, ctx):
        # self.visitChildren(ctx)
        #  getting context children
        children = ctx.children
        record_calls = []

        #  if modifiable primary is a variable name
        if len(children) == 1:
            identifier = self.unicode_to_str(children[0].getText())
            #  check if variable was declared
            if not self.current_symbol_table.is_defined_in_scope(identifier):
                raise Exception('Variable {} is not defined'.format(identifier))
            #  return type of the variable from the symbol table
            return self.current_symbol_table.get_variable_info(identifier).variable_type
        #  if modifiable primary is a array identifier
        elif type(children[2]) is HelloParser.ExpressionContext:
            array_identifier = self.unicode_to_str(children[0].getText())
            #  check if array was declared
            if not self.current_symbol_table.is_defined_in_scope(array_identifier):
                raise Exception('Array with name {} is not defined'.format(array_identifier))
            #  return type of the array from the symbol table
            return TypeTable.get_type(
                self.current_symbol_table.get_variable_info(array_identifier).variable_type).nested_type_id
        #  if modifiable primary is a record field access
        else:
            #  append identifiers of records and their fields to a list
            for i in range(len(children)):
                if i % 2 == 0:
                    identifier = self.unicode_to_str(children[i].getText())
                    # check that the first identifier is a declared variable with type record
                    if i == 0 and not self.current_symbol_table.is_defined_in_scope(identifier):
                        raise Exception('Record with name {} is not defined'.format(identifier))
                    record_calls.append(identifier)
            #  check validity of field calls
            type_id = self.current_symbol_table.get_variable_info(record_calls[0]).variable_type
            current_type = self.type_table.table[type_id]
            for i in range(len(record_calls) - 1):
                if record_calls[i + 1] not in current_type.inner_declarations.keys():
                    raise Exception(
                        "Record {} doesn't have a field {}".format(record_calls[i], record_calls[i + 1]))
                type_id = current_type.inner_declarations[record_calls[i + 1]]
                current_type = self.type_table.table[type_id]
            return type_id

    # Visit a parse tree produced by HelloParser#eos.
    def visitEos(self, ctx):
        return self.visitChildren(ctx)
