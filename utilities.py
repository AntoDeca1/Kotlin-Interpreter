def enter_scope(symbol_tables):
    '''
    We imagine our symbol table as a list of dictionaries.
    :param symbol_tables:
    :return:
    '''
    symbol_tables.append({})


def exit_scope(symbol_tables):
    """
    We simply remove one dictionary, so we exit the current scope
    :param symbol_tables:
    :return:
    """
    symbol_tables.pop()


def register_variable(name, type, value, symbol_tables):
    """
    We add a variable to our symbol table
    :param name: Variable name
    :param type: Variable type
    :param value: Value of the variable
    :param symbol_tables: List of dictionaries(We access the one on the top)
    :return:
    """
    current_symbol_table = symbol_tables[-1]
    if name in current_symbol_table:
        raise Exception(f"Variabile {name} già dichiarata nello scope corrente")
    current_symbol_table[name] = (type, value)


def find_variable(name, symbol_tables):
    """
    We search into the scopes,starting from the inner scope
    :param name:
    :param symbol_tables:
    :return:
    """
    for symbol_table in reversed(symbol_tables):
        if name in symbol_table:
            return symbol_table[name]
    raise Exception(f"Variabile {name} non dichiarata")


def get_type(x):
    """
    Function to return the type
    :param x:
    :return:
    """
    if type(x) == "<class 'str'>":
        return "String"
    elif type(x) == "<class 'int'>":
        return "Int"
    elif type(x) == "<class 'bool'>":
        return "Boolean"
