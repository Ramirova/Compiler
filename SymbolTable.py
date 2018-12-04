class SymbolTable:

    root_table = None

    def __init__(self, parent):
        # if not (SymbolTable.root_table is not None and parent is None):
        #     raise Exception
        if parent is None and SymbolTable.root_table is None:
            SymbolTable.root_table = self
        self.parent_scope = parent
        self.scope = {}
        self.child_scopes = {}
        self.routines = {}
        self.routine_inner_scopes_counter = 0

    def get_variable_info(self, variable_name):
        if self.parent_scope is None and not self.is_defined_in_scope(variable_name):
            raise Exception('there is no {} variable defined'.format(variable_name))
        if self.is_defined_in_current_scope(variable_name):
            return self.scope[variable_name]
        else:
            return self.parent_scope.get_variable_info(variable_name)

    def get_routine_info(self, routine_name):
        if self.parent_scope is None and not self.routine_defined_in_scope(routine_name):
            raise Exception('there is no {} routine defined'.format(routine_name))
        if self.routine_defined_in_current_scope(routine_name):
            return self.routines[routine_name]
        else:
            return self.parent_scope.get_routine_info(routine_name)

    def add(self, variable_name, variable_type):
        self.scope[variable_name] = SymbolTableEntry(False, variable_type, variable_name)

    def add_routine(self, routine_name, parameters, return_type):
        self.routines[routine_name] = RoutineTableEntry(routine_name, parameters, return_type)

    def remove(self, variable_name):
        del self.scope[variable_name]

    def set_used(self, variable_name):
        if not self.is_defined_in_scope(variable_name):
            raise Exception
        else:
            self.scope[variable_name].used = True

    def create_child_scope(self, scope_name):
        self.child_scopes[scope_name] = SymbolTable(self)
        return self.child_scopes[scope_name]

    def remove_child_scope(self, scope_name):
        del self.child_scopes[scope_name]

    def routine_defined_in_current_scope(self, routine_name):
        if routine_name not in self.routines.keys():
            return False
        else:
            return True

    def routine_defined_in_scope(self, routine_name):
        if routine_name not in self.routines.keys():
            if self.parent_scope is not None:
                return self.parent_scope.routine_defined_in_scope(routine_name)
            else:
                return False
        else:
            return True

    def is_defined_in_scope(self, variable_name):
        if variable_name not in self.scope.keys():
            if self.parent_scope is not None:
                return self.parent_scope.is_defined_in_scope(variable_name)
            else:
                return False
        else:
            return True

    def is_defined_in_current_scope(self, variable_name):
        return self.aux_is_defined_in_current_scope(variable_name, self.parent_scope is None)

    def aux_is_defined_in_current_scope(self, variable_name, is_root_scope):
        if is_root_scope:
            return variable_name in self.routines.keys()

        if variable_name not in self.routines.keys():
            if self.parent_scope.parent_scope is not None:
                return self.parent_scope.aux_is_defined_in_current_scope(variable_name, is_root_scope)
            else:
                return False
        else:
            return True


class SymbolTableEntry:
    def __init__(self, used, variable_type, variable_name):
        self.used = used
        # self.initializer = initializer
        self.variable_type = variable_type
        self.variable_name = variable_name
        # self.value = value


class RoutineTableEntry:
    def __init__(self, name, parameters, return_type):
        self.name = name
        self.parameters = parameters
        self.return_type = return_type


