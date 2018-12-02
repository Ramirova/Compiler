class TypeTable:
    """
    The table which contains all types defined in the global scope.
    There are three possible kinds of types: Primitives, Arrays, Records.

    The table itself is a dictionary, where keys are ids of types (can be gotten in the classes of types)
    The first three keys - 1, 2, 3 are reserved for the primitives types: integer, real and boolean respectively.

    The whole description of the types can be found in the corresponding classes.

    The table itself is singleton and should bbe accessed
    """

    def __init__(self):
        pass

    table = {}

    @staticmethod
    def add_type(type_id, type_content):
        TypeTable.table[type_id] = type_content


class PrimitiveType:
    """
    This class represents primitive type. It is only needed as enumerator. To reference a primitive type, simply
    use its id as defined in this class
    """

    integer = 1
    real = 2
    boolean = 3

    types = {'integer': 1, 'real': 2, 'boolean': 3}

    def __init__(self):
        pass


class ArrayType:
    """
    This class represents array type. It contains self.nested_type_id which is the type of elements in array.
    The new type is automatically added to the Type table whenever a new type object is created
    """

    def __init__(self, nested_type):
        """
        :param nested_type: id of the type of the elements in the array
        """

        self.nested_type_id = 0

        if type(nested_type) is PrimitiveType:
            self.nested_type_id = nested_type

        if type(nested_type) is ArrayType:
            self.nested_type_id = nested_type.get_id()

        if type(nested_type) is RecordType:
            self.nested_type_id = nested_type.get_id()

        TypeTable.table[self.get_id()] = self

    def get_id(self):
        return hash(self.nested_type_id)


class RecordType:
    """
    This class represents array type. It contains self.nested_type_id which is the type of elements in array.
    The new type is automatically added to the Type table whenever a new type object is created.
    """

    def __init__(self, variable_dict):
        """
        :param variable_dict: a dictionary where the keys are the names of the variables in the record and the values
        are ids of their types.
        """
        self.inner_declarations = variable_dict
        TypeTable.table[self.get_id()] = self

    def get_id(self):
        return hash(frozenset(self.inner_declarations.items()))


class AliasType:
    """
    This class represents mapping between identifier (alias) name and its type id
    """

    table = {}

    def __init__(self):
        pass
