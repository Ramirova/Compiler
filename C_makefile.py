"""
Class writes to C file the result of code generation in appropriate order (type definitions, declarations, main method)
"""
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
        file.write("#include <stdio.h>\n")

        for typedef in self.typedef_queue:
            file.write(typedef)
        file.write("\n")

        for main_part in self.main_queue:
            file.write(main_part)
        file.write("\n")

        file.write(self.make_main())
        file.close()

    def make_main(self):
        """
        Method makes main method
        :return: string with main method of the C program
        """
        main = ""
        main += "int main (int argc, char *argv[]) {\n"
        main += "if argc > 0 {\n"
        main += "switch(argv[0]) {\n"

        # main += "const char *routines[" + len(self.routines) + "] = { "
        for i in range(len(self.routines)):
            main += "case " + self.routines[i] + ":\n"
            main += self.routines[i] + "(argv)\n"
            main += "break;\n"
        main += "default:\n break;\n}\n}"
        return main