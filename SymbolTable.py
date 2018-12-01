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

    def add(self, variable_name, variable_type):
        self.scope[variable_name] = SymbolTableEntry(False, variable_type, variable_name)

    def add_routine(self, routine_name):
        self.routines[routine_name] = routine_name

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


class SymbolTableEntry:
    def __init__(self, used, variable_type, variable_name):
        self.used = used
        # self.initializer = initializer
        self.variable_type = variable_type
        self.variable_name = variable_name
        # self.value = value

