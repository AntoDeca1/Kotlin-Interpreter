def get_type(x):
    """
    Function to infer the type
    :param x: Expression
    :return: Type
    """
    if str(type(x)) == "<class 'str'>":
        return "String"
    elif str(type(x)) == "<class 'int'>":
        return "Int"
    elif str(type(x)) == "<class 'bool'>":
        return "Boolean"


def is_changeable(val_type):
    """
    Checks if the variable could be reassigned
    :param val_type: var || val
    """
    if val_type == "var":
        return True
    else:
        return False


def string_concatenation(operator_1, operator_2):
    """
    Following the Kotlin behaviour applies string concatenation
    """
    return operator_1 + str(operator_2)
