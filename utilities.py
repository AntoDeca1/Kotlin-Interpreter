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

