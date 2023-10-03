class SymbolTable:
    def __init__(self):
        self.symbol_tables = [{}]

    def enter_scope(self):
        '''
        We imagine our symbol table as a list of dictionaries.
        :param symbol_tables:
        :return:
        '''
        self.symbol_tables.append({})

    def exit_scope(self):
        """
        We simply remove one dictionary, so we exit the current scope
        :param symbol_tables:
        :return:
        """
        self.symbol_tables.pop()

    def register_variable(self, name, type, value):
        """
        We add a variable to our symbol table
        :param name: Variable name
        :param type: Variable type
        :param value: Value of the variable
        :param symbol_tables: List of dictionaries(We access the one on the top)
        :return:
        """
        current_symbol_table = self.symbol_tables[-1]
        if name in current_symbol_table:
            raise Exception(f"Variabile {name} già dichiarata nello scope corrente")
        current_symbol_table[name] = (type, value)

    def find_variable(self, name):
        """
        We search into the scopes,starting from the inner scope
        :param name:
        :param symbol_tables:
        :return:
        """
        for symbol_table in reversed(self.symbol_tables):
            if name in symbol_table:
                return symbol_table[name]
        raise Exception(f"Variabile {name} non dichiarata")

    def modify_variable(self, name, new_value, type):
        found = False
        for symbol_table in reversed(self.symbol_tables):
            if name in symbol_table:
                symbol_table[name] = (type, new_value)
                found = True
        if found == False:
            raise Exception(f"Variabile {name} non dichiarata")
