class TypeMismatch(Exception):
    def __init__(self, messaggio):
        super().__init__(messaggio)


class ParamatersMismatch(Exception):
    def __init__(self, messaggio):
        super().__init__(messaggio)


class VariableNotDeclared(Exception):
    def __init__(self, messaggio):
        super().__init__(messaggio)


class VariableAlreadyDeclared(Exception):
    def __init__(self, messaggio):
        super().__init__(messaggio)


class VariableNotModifiable(Exception):
    def __init__(self, messaggio):
        super().__init__(messaggio)


class MainException(Exception):
    def __init__(self, messaggio):
        super().__init__(messaggio)
