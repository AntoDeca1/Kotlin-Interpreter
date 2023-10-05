def get_type(x):
    """
    Function to return the type
    :param x:
    :return:
    """
    if str(type(x)) == "<class 'str'>":
        return "String"
    elif str(type(x)) == "<class 'int'>":
        return "Int"
    elif (type(x)) == "<class 'bool'>":
        return "Boolean"


def is_changeable(val_type):
    if val_type == "var":
        return True
    else:
        return False


def string_concatenation(operator_1, operator_2):
        return operator_1 + str(operator_2)
