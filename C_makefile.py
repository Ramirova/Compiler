"""
Class writes to C file the result of code generation in appropriate order (type definitions, declarations, main method)
"""
from SymbolTable import *


class C_makefile:
    def __init__(self, typedef_queue, main_queue, routines):
        """
        Class initializer
        :param typedef_queue: list with type definitions in C
        :param main_queue: list with declarations of variables and routines in C
        :param routines: list with names of the routines
        """
        self.typedef_queue = typedef_queue
        self.main_queue = main_queue
        self.routines = routines

    def make_file(self):
        """
        Method makes the resulting file
        :return:
        """
        file = open("c_file.c", "w+")
        file.write("#include <stdio.h>\n#include <stdbool.h>\n#include <string.h>\n")

        for typedef in self.typedef_queue:
            file.write(typedef)
        file.write("\n")

        for main_part in self.main_queue:
            file.write(main_part)
        file.write("\n")

        file.write(self.make_main())
        file.close()

    def get_bool_handler_function(self):
        return "const char * bool_hadler(int arg) { if arg == 1 return \"true\" else return \"false\""

    def make_main(self):
        """
        Method makes main method
        :return: string with main method of the C program
        """
        main = ""
        main += "int main (int argc, char *argv[]) {\n"
        main += "if (argc > 1) {\n"

        # main += "const char *routines[" + len(self.routines) + "] = { "
        for i in range(len(self.routines)):
            parameters = SymbolTable.root_table.get_routine_info(routine_name=self.routines[i]).parameters
            if len(filter(lambda x: (x < 0 or x > 3), parameters)) == 0:
                main += "if (strcmp(argv[1], \"" + self.routines[i] + "\") > 0) {\n"
                main += self.routines[i]
                if parameters is None:
                    main += '();\n'
                else:
                    main += "("
                    for j in range(len(parameters)):
                        main += self.get_param_type(parameters[j]) + "argv[" + str(j + 2) + "], "
                    main = main[:-2]
                    main += ");\n"
                main += "}\n"
        main += "\n}\n}"
        return main

    def get_param_type(self, type_id):
        if type_id == 1:
            return "(int) "
        elif type_id == 2:
            return "(double) "
        elif type_id == 3:
            return "(bool) "
        return ""
