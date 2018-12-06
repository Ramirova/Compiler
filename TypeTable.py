from collections import deque
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

    table = {}  # Table with types
    aux_table = deque()  # expression types are saved here

    @staticmethod
    def add_type(type_id, type_content):
        TypeTable.table[type_id] = type_content

    @staticmethod
    def add_aux_type(type_id):
        TypeTable.aux_table.append(type_id)

    @staticmethod
    def get_aux_type():
        return TypeTable.aux_table.popleft()

    @staticmethod
    def get_type_name(type_id):
        """
        :param type_id:
        :return: a string representation of the type
        """
        if type_id not in TypeTable.table.keys():
            raise Exception("cannot find type with id {}".format(type_id))
        type_name = TypeTable.table[type_id].__class__.__name__
        if type_name == 'PrimitiveType':
            return '{}'.format(PrimitiveType.type_names[type_id])
        if type_name == 'ArrayType':
            return '<{} of {}>'.format(type_name, TypeTable.get_type_name(TypeTable.table[type_id].nested_type_id))
        if type_name == 'RecordType':
            result_string = '<' + type_name + ' with inner variables: \n{'
            for key, value in TypeTable.table[type_id].inner_declarations.items():
                result_string += '{}: {} \n'.format(key, TypeTable.get_type_name(value))
            return result_string + '}>'


    @staticmethod
    def get_type(type_id):
        """
        :param type_id:
        :return: object of type
        """
        if type_id not in TypeTable.table.keys():
            raise Exception("cannot find type with id {}".format(type_id))
        return TypeTable.table[type_id]


class PrimitiveType:
    """
    This class represents primitive type. It is only needed as enumerator. To reference a primitive type, simply
    use its id as defined in this class
    """

    integer = 1
    real = 2
    boolean = 3

    types = {'integer': 1, 'real': 2, 'boolean': 3}
    type_names = {1: 'integer', 2: 'real', 3: 'boolean'}

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

        self.nested_type_id = nested_type

        TypeTable.table[self.get_id()] = self

    def get_id(self):
        return hash(frozenset({0: self.nested_type_id}.items()))


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

    # @staticmethod
    # def get_type_of_alias(alias_name):
    #     if alias_name in

    def __init__(self):
        pass


class TypeUtils:
    """
    Contains several useful functions to work with types
    """
    def __init__(self):
        pass

    @staticmethod
    def are_compatible_for_assignment(type_id_1, type_id_2):
        if type_id_1 == type_id_2:
            return True

        if type_id_1 == PrimitiveType.boolean and type_id_2 == PrimitiveType.real:
            return False

        if type_id_1 in [1, 2, 3] and type_id_2 in [1, 2, 3]:
            return True

        return False

    @staticmethod
    def are_compatible(type_id_1, type_id_2):
        if type_id_1 == type_id_2:
            return True

        if type_id_1 in [1, 2, 3] and type_id_2 in [1, 2, 3]:
            return True

        return False

    @staticmethod
    def is_primitive(type_id):
        return type_id in [1, 2, 3]

    @staticmethod
    def deduce_type(type_id_1, type_id_2):
        if type_id_1 == PrimitiveType.integer and type_id_2 == PrimitiveType.integer:
            return PrimitiveType.integer
        if type_id_1 == PrimitiveType.integer and type_id_2 == PrimitiveType.real\
                or type_id_1 == PrimitiveType.real and type_id_2 == PrimitiveType.integer:
            return PrimitiveType.real
        if type_id_1 == PrimitiveType.integer and type_id_2 == PrimitiveType.boolean\
                or type_id_1 == PrimitiveType.boolean and type_id_2 == PrimitiveType.integer:
            return PrimitiveType.integer
        if type_id_1 == PrimitiveType.real and type_id_2 == PrimitiveType.real:
            return PrimitiveType.real
        if type_id_1 == PrimitiveType.real and type_id_2 == PrimitiveType.boolean\
                or type_id_1 == PrimitiveType.boolean and type_id_2 == PrimitiveType.real:
            return PrimitiveType.real
        if type_id_1 == PrimitiveType.boolean and type_id_2 == PrimitiveType.boolean:
            return PrimitiveType.integer
        raise Exception("Incompatible types {} and {}. This operator can only be applied to primitive types"
                        .format(TypeTable.get_type_name(type_id_1), TypeTable.get_type_name(type_id_2)))

    @staticmethod
    def deduce_type_division(type_id_1, type_id_2):
        if type_id_1 == PrimitiveType.integer and type_id_2 == PrimitiveType.integer:
            return PrimitiveType.real
        if type_id_1 == PrimitiveType.integer and type_id_2 == PrimitiveType.real \
                or type_id_1 == PrimitiveType.real and type_id_2 == PrimitiveType.integer:
            return PrimitiveType.real
        if type_id_1 == PrimitiveType.integer and type_id_2 == PrimitiveType.boolean \
                or type_id_1 == PrimitiveType.boolean and type_id_2 == PrimitiveType.integer:
            return PrimitiveType.real
        if type_id_1 == PrimitiveType.real and type_id_2 == PrimitiveType.real:
            return PrimitiveType.real
        if type_id_1 == PrimitiveType.real and type_id_2 == PrimitiveType.boolean \
                or type_id_1 == PrimitiveType.boolean and type_id_2 == PrimitiveType.real:
            return PrimitiveType.real
        if type_id_1 == PrimitiveType.boolean and type_id_2 == PrimitiveType.boolean:
            return PrimitiveType.boolean
        raise Exception("Incompatible types {} and {}. This operator can only be applied to primitive types"
                        .format(TypeTable.get_type_name(type_id_1), TypeTable.get_type_name(type_id_2)))

    @staticmethod
    def deduce_type_module(type_id_1, type_id_2):
        if type_id_1 == PrimitiveType.integer and type_id_2 == PrimitiveType.integer:
            return PrimitiveType.integer
        raise Exception('cannot take module for {} and {}. Module can only be applied to integer values'
                        .format(TypeTable.get_type_name(type_id_1), TypeTable.get_type_name(type_id_2)))

    @staticmethod
    def deduce_type_comparable(type_id_1, type_id_2):
        if type_id_1 in [1, 2, 3] and type_id_2 in [1, 2, 3]:
            return True
        raise Exception("Incompatible types {} and {} for comparison. This operator can only be applied to primitive"
                        " types".format(TypeTable.get_type_name(type_id_1), TypeTable.get_type_name(type_id_2)))
