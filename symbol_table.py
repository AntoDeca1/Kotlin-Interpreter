from utilities import *
from exceptions import *


class SymbolTable:
    def __init__(self):
        """
        Imagine our symbol table as a list of dictionaries.
        """
        self.symbol_tables = [{}]

    def enter_scope(self):
        """
        Enter a new scope by simply appending a new dictionary in the list
        """
        self.symbol_tables.append({})

    def exit_scope(self):
        """
        Simply remove one dictionary, so we exit the current scope
        """
        self.symbol_tables.pop()

    def register_variable(self, name, type, value, is_Var, lineno=None):
        """
        Add a variable to our symbol table
        :param name: Variable name
        :param type: Variable type
        :param value: Value of the variable
        :param is_Var: Keeps track if the variable is initialized as Var or Val
        """
        current_symbol_table = self.symbol_tables[-1]
        if name in current_symbol_table:
            raise VariableAlreadyDeclared(
                f" Error at line {lineno} Variable {name} already declared in the current scope")
        current_symbol_table[name] = (type, value, is_Var)

    def clean_scope(self):
        """
        Function that clean the scope
        Used in: WhileLoopNode,ForLoopNode (visit.py)
        :return:
        """
        self.symbol_tables[-1] = {}

    def find_variable(self, name, lineno=None):
        """
        Search into the scopes,starting from the inner scope, return the first occurrence
        :param name: Variable name
        """
        for symbol_table in reversed(self.symbol_tables):
            if name in symbol_table:
                return symbol_table[name]
        raise VariableNotDeclared(f" Error at line {lineno}:  Variable {name} not declared")

    def modify_variable(self, name, new_value, lineno=None):
        """
        Modify the value of the specified variable in all the scopes starting from the inner one
        :param name: Variable name
        :param new_value: New value
        """
        found = False
        for symbol_table in reversed(self.symbol_tables):
            if name in symbol_table:
                type, _, variable_type = symbol_table[name]
                if is_changeable(variable_type):
                    symbol_table[name] = (type, new_value, variable_type)
                    return
                else:
                    raise VariableNotModifiable(f" Error at line {lineno}: Val variables are not modifiable")
        if found == False:
            raise VariableNotDeclared(f" Error at line {lineno}: Variable {name} not declared")


class FunctionTable(SymbolTable):
    def __init__(self):
        super().__init__()

    def register_function(self, name, parameter_list, statament_list, output_type=None, lineno=None):
        """
        Add a function to the current function table
        :param name: Function ID
        :param parameter_list: List of parameters
        :param statament_list: List of statements in the function body
        :param output_type: Output type
        """
        current_symbol_table = self.symbol_tables[-1]
        if name in current_symbol_table:
            raise VariableAlreadyDeclared(
                f" Error at line {lineno}: Function {name} already declared in the current scope")
        current_symbol_table[name] = (parameter_list, statament_list, output_type, lineno)
