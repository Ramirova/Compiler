import copy

class SymbolTable:
    """
    This class represents symbol table. It supports supports a hierarchy of tables, that correspond to
    """
    root_table = None  # singleton which has the instance for the root table
    aux_root_table = None  # a dummy root table, needed in some cases for compatibility
    inner_scope_name = 'inner_scope_'

    def __init__(self, parent):
        if parent is None and SymbolTable.root_table is None:
            SymbolTable.root_table = self
            SymbolTable.aux_root_table = copy.deepcopy(self)
        self.parent_scope = parent
        self.scope = {}
        self.child_scopes = {}
        self.routines = {}
        self.routine_inner_scopes_counter = 0

    def get_variable_info(self, variable_name):
        """
        :param variable_name: name of the variable
        :return: object of type SymbolTableEntry containing information about the requested variable
        """
        if self.parent_scope is None and not self.is_defined_in_scope(variable_name):
            raise Exception('there is no {} variable defined'.format(variable_name))
        if variable_name in self.scope.keys():
            return self.scope[variable_name]
        else:
            return self.parent_scope.get_variable_info(variable_name)

    def get_routine_info(self, routine_name):
        """
        :param routine_name:
        :return: object of type RoutineTableEntry containing information about the requested routine
        """
        if self.parent_scope is None and not self.routine_defined_in_scope(routine_name):
            raise Exception('there is no {} routine defined'.format(routine_name))
        if self.routine_defined_in_scope(routine_name):
            return SymbolTable.root_table.routines[routine_name]

    def add_variable(self, variable_name, variable_type):
        """
        Adds new variable
        :param variable_name:
        :param variable_type:
        :return:
        """
        self.scope[variable_name] = SymbolTableEntry(variable_type, variable_name)

    def add_routine(self, routine_name, parameters, return_type):
        """
        :param routine_name:
        :param parameters: an ordered list of ids of types of parameters (in the same order as they occur in
                            routine definition)
        :param return_type:
        """
        if not self.is_root_table():
            raise Exception('Routines can only be added to the global scope, i.e. to the root table')
        self.routines[routine_name] = RoutineTableEntry(routine_name, parameters, return_type)

    def remove(self, variable_name):
        del self.scope[variable_name]

    def set_used(self, variable_name):
        if not self.is_defined_in_scope(variable_name):
            raise Exception
        else:
            self.scope[variable_name].used = True

    def create_child_scope(self, scope_name):
        """
        Create a new child scope for the current symbol table.
        :param scope_name:
        :return: the created child scope
        """
        self.child_scopes[scope_name] = SymbolTable(self)
        return self.child_scopes[scope_name]

    def remove_child_scope(self, scope_name):
        """
        Deletes the given child scope of the current symbol table
        :param scope_name:
        """
        del self.child_scopes[scope_name]

    def routine_defined_in_scope(self, routine_name):
        """
        :param routine_name:
        :return: whether the routine is defined
        """
        return routine_name in SymbolTable.root_table.routines.keys()

    def is_defined_in_scope(self, variable_name):
        if variable_name not in self.scope.keys():
            if self.parent_scope is not None:
                return self.parent_scope.is_defined_in_scope(variable_name)
            else:
                return False
        else:
            return True

    def is_defined_in_current_scope(self, variable_name):
        """
        :param variable_name:
        :return: whether variable is defined in current scope (scopes of if, while and for are considered
                 to be in the same scope of routine)
        """
        return self.aux_is_defined_in_current_scope(variable_name, self.parent_scope is None)

    def aux_is_defined_in_current_scope(self, variable_name, is_root_scope):
        if is_root_scope:
            return variable_name in self.scope.keys()

        if variable_name not in self.scope.keys():
            if self.parent_scope.parent_scope is not None:
                return self.parent_scope.aux_is_defined_in_current_scope(variable_name, is_root_scope)
            else:
                return False
        else:
            return True

    def get_new_inner_scope_name(self):
        """
        :return: a new name for the next inner scope of the current scope
        """
        if self.parent_scope is None:
            raise Exception("While, for and if cannot be used in the global scope. Cannot create a general"
                            "inner scope for global scope, only one for a routine")
        self.routine_inner_scopes_counter += 1
        return "{}{}".format(SymbolTable.inner_scope_name, self.routine_inner_scopes_counter)

    def is_root_table(self):
        """
        :return: true if the table object is the root table, false otherwise
        """
        return self.parent_scope is None

    def reset_counter(self):
        self.routine_inner_scopes_counter = 0

    @staticmethod
    def reset_counters(current_table=None):
        """
        Resets all counters in all tables in the hierarchy.
        :param current_table:
        """
        if current_table is None:
            current_table = SymbolTable.root_table
        current_table.reset_counter()
        for child_table in current_table.child_scopes.values():
            SymbolTable.reset_counters(child_table)


class SymbolTableEntry:
    """
    Represents a single tale entry in a symbol table
    """
    def __init__(self, variable_type, variable_name):
        """
        :param variable_type: id of the type
        :param variable_name: name of the variable
        """
        self.variable_type = variable_type
        self.variable_name = variable_name


class RoutineTableEntry:
    """
    Represents a single table entry in the routine table
    """
    def __init__(self, name, parameters, return_type):
        """
        :param name:
        :param parameters: an ordered list with ids of types of the parameters
        :param return_type: id of the return type (can be None)
        """
        self.name = name
        self.parameters = parameters
        self.return_type = return_type
