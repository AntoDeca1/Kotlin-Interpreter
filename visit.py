from symbol_table import *
from utilities import *
import sys
from exceptions import *

sys.tracebacklimit = 0


class Visitor:
    def __init__(self, s_t, f_t):
        """
        Visit the AST checking for semantic errors
        :param s_t: variable symbol tables
        :param f_t: function symbol tables
        """
        self.s_t = s_t
        self.f_t = f_t

    def visit(self, node):
        """
        Recursively visit the AST managing the scopes checking for possibles
        semantic errors
        :param node: Current node in the recursion
        """
        try:
            if node.node_type == "ProgramNode":
                result = self.visit(node.children[0])
                self.visit(self.check_if_main())
                return result
            elif node.node_type == "StatementList":
                for children in node.children:
                    result = self.visit(children)
                    if result is not None:
                        return result
                return
            elif node.node_type == "VariableDeclarationNode":
                id = self.visit(node.children[0])
                if len(node.children) == 3:
                    type = self.visit(node.children[1])
                    expression = self.visit(node.children[2])
                    if type != get_type(expression):
                        raise TypeMismatch(
                            f" Error at line {node.children[1].lineno}: Inferred type is {get_type(expression)} but {type} was expected")
                else:
                    expression = self.visit(node.children[1])
                    type = get_type(expression)
                self.s_t.register_variable(id, type, expression, node.leaf, lineno=node.children[0].lineno)
            elif node.node_type == "WhileStatementNode":
                self.s_t.enter_scope()
                while self.visit(node.children[0]):
                    self.visit(node.children[1])
                    self.s_t.clean_scope()
                self.s_t.exit_scope()
                return
            elif node.node_type == "ForStatement":
                self.s_t.enter_scope()
                id, range_list, step = self.visit(node.children[0])
                self.s_t.register_variable(id, 'Int', range_list[0], 'val')
                for i in range_list:
                    self.visit(node.children[1])
                    self.s_t.clean_scope()
                    self.s_t.register_variable(id, 'Int', i + step, 'val')
                self.s_t.exit_scope()
            elif node.node_type == "If-else-StatementNode":
                condition = self.visit(node.children[0])
                if get_type(condition) != "Boolean":
                    raise TypeMismatch(
                        f" Error at line {node.children[0].lineno} The integer literal does not conform to the expected type Boolean")
                if condition:
                    self.s_t.enter_scope()
                    statement_list = self.visit(node.children[1])
                    self.s_t.exit_scope()
                    return statement_list
                else:
                    self.s_t.enter_scope()
                    statement_list = self.visit(node.children[2])
                    self.s_t.exit_scope()
                    return statement_list
            elif node.node_type == "IfStatementNode":
                condition = self.visit(node.children[0])
                if get_type(condition) != "Boolean":
                    raise TypeMismatch(
                        f"Error at line {node.children[0].lineno}:The integer literal does not conform to the expected type Boolean")
                if condition:
                    self.s_t.enter_scope()
                    statement_list = self.visit(node.children[1])
                    self.s_t.exit_scope()
                    return statement_list
            elif node.node_type == "AssignmentNode":
                id = self.visit(node.children[0])
                value = self.visit(node.children[1])
                type = get_type(value)
                variable_type = self.s_t.find_variable(id, lineno=node.children[0].lineno)[0]
                if variable_type == type:
                    self.s_t.modify_variable(id, value, lineno=node.children[0].lineno)
                else:
                    raise TypeMismatch(
                        f" Error at line {node.children[1].lineno} Inferred type is {type} but {variable_type} was expected")
                return
            elif node.node_type == "FunctionDeclarationNode":
                function_name = self.visit(node.children[0])
                parameter_list = self.visit(node.children[1])
                if len(node.children) == 4:
                    output_type = self.visit(node.children[2])
                    stataments_list = node.children[3]
                    self.f_t.register_function(function_name, parameter_list, stataments_list, output_type,
                                               lineno=node.children[0].lineno)
                else:
                    stataments_list = node.children[2]
                    self.f_t.register_function(function_name, parameter_list, stataments_list,
                                               lineno=node.children[0].lineno)
                return
            elif node.node_type == "FunctionCallingNode":
                function_name = self.visit(node.children[0])
                input_parameters = self.visit(node.children[1])
                parameter_list, statament_list, output_type, lineno = self.f_t.find_variable(function_name,
                                                                                             node.children[0].lineno)
                if parameter_list is None and input_parameters is None:
                    self.s_t.enter_scope()
                    result = self.visit(statament_list)
                    result_type = get_type(result)
                    if self.check_type_match(result_type, output_type, statament_list, lineno): return result
                elif parameter_list is None and input_parameters is not None:
                    raise ParamatersMismatch(
                        f" Error at line {node.children[0].lineno} : Too many arguments for local fun {function_name}")
                elif parameter_list is not None and input_parameters is None:
                    raise ParamatersMismatch(
                        f" Error at line {node.children[0].lineno} : No value passed for parameters {parameter_list}")
                input_types = [get_type(parameter) for parameter in input_parameters]
                correct_types = [parameter[1] for parameter in parameter_list]
                if input_types == correct_types:
                    self.s_t.enter_scope()
                    for parameter_input, parameter_declared in zip(parameter_list, input_parameters):
                        name, type = parameter_input
                        self.s_t.register_variable(name, type, parameter_declared, 'val',
                                                   lineno=node.children[0].lineno)
                    result = self.visit(statament_list)
                    result_type = get_type(result)
                    if self.check_type_match(result_type, output_type, statament_list, lineno): return result
                else:
                    raise ParamatersMismatch(
                        f" Error at line {node.children[0].lineno}: Parameters Mismatch in fun {function_name}").with_traceback(
                        None) from None
            elif node.node_type == "RangeOperator":
                id = self.visit(node.children[0])
                term_from = node.children[1]
                term_to = node.children[2]
                step = 1
                term_from = self.check_if_st(term_from)
                term_to = self.check_if_st(term_to)
                if len(node.children) == 4:
                    step = node.children[3]
                    step = self.check_if_st(step)
                range_list = list(range(term_from, term_to + 1, step))
                return (id, range_list, step)
            elif node.node_type == "ReturnNode":
                return self.check_if_st(node.children[0])
            elif node.node_type == "ParameterDeclarationNode":
                parameter_name = self.visit(node.children[0])
                parameter_type = self.visit(node.children[1])
                return (parameter_name, parameter_type)
            elif node.node_type == "ParameterListCalling":
                parameters = []
                for children in node.children:
                    temp_parameter = self.check_if_st(children)
                    parameters.append(temp_parameter)
                return parameters
            elif node.node_type == "ParameterListDeclaration":
                parameters = []
                for children in node.children:
                    temp_parameter = self.visit(children)
                    parameters.append(temp_parameter)
                return parameters
            elif node.node_type == "PrintStatementNode":
                print(self.check_if_st(node.children[0]))
                return
            elif node.node_type == "ReadlineNode":
                result = input()
                return result
            elif node.node_type == "TermNode":
                return node.leaf
            elif node.node_type == "EmptyNode":
                return
            elif node.node_type == "ExpressionNode":
                return self.visit(node.children[0])
            elif node.node_type == "BinaryExpressionNode":
                return self.binary_expression(node)
            elif node.node_type == "UnaryExpressionNode":
                operator = node.leaf
                if operator == "-":
                    return -(self.check_if_st(node.children[0]))
                else:
                    return not (self.check_if_st(node.children[0]))
            elif node.node_type == "TypeNode":
                return node.leaf
            elif node.node_type == "LiteralNode":
                return node.leaf
        except (TypeMismatch, ParamatersMismatch, VariableNotDeclared, VariableAlreadyDeclared, MainException,
                VariableNotModifiable, Exception) as e:
            print(f"Exception: {e}")
            sys.exit(1)

    def binary_expression(self, node):
        """
        Management of the binary expressions
        :param node: Expression node
        :return: Result
        """
        first_operator = self.check_if_st(node.children[0], node.children[0].lineno)
        second_operator = self.check_if_st(node.children[1], node.children[1].lineno)
        try:
            if node.leaf == "+":
                if get_type(first_operator) == "String":
                    return string_concatenation(first_operator, second_operator)
                return first_operator + second_operator
            elif node.leaf == "-":
                return first_operator - second_operator
            elif node.leaf == "*":
                return first_operator * second_operator
            elif node.leaf == "/":
                return first_operator / second_operator
            elif node.leaf == ">=":
                return first_operator >= second_operator
            elif node.leaf == "<=":
                return first_operator <= second_operator
            elif node.leaf == "<":
                return first_operator < second_operator
            elif node.leaf == ">":
                return first_operator > second_operator
            elif node.leaf == "==":
                return first_operator == second_operator
            elif node.leaf == "&&":
                return first_operator and second_operator
            elif node.leaf == "||":
                return first_operator or second_operator
            elif node.leaf == "!=":
                return first_operator != second_operator
        except Exception as e:
            raise TypeMismatch(f"Error at line At line {node.lineno} : {e} ").with_traceback(None) from None

    def check_type_match(self, result_type, output_type, statement_list, function_decl_line):
        lineno = function_decl_line
        last_child = None
        if statement_list.node_type != "EmptyNode":
            last_child = statement_list.children[-1]
        if last_child and last_child.node_type == "ReturnNode":
            lineno = statement_list.children[-1].lineno
        if result_type != output_type:
            raise TypeMismatch(
                f": Error at line {lineno}  Type Mismatch: The declared output type does not conform with the real one").with_traceback(
                None) from None
        else:
            self.s_t.exit_scope()
            return True

    def check_if_main(self):
        """
        Check if the main declaration is present, if not raise an exception
        """
        try:
            parameter_list, statament_list, output_type, _ = self.f_t.find_variable('main')
            return statament_list
        except Exception as e:
            raise MainException("Expecting a main declaration")

    def check_if_st(self, node, lineno=None):
        """
        Since a term node could be both an ID or a literal,
        if it is an ID search for an occurrency in the symbol table and retrieve its value,
        if it is a literal node simply visits it in order to retrieve its value.
        The exceptions are managed in the find_variable function.
        """
        if node.node_type == "TermNode":
            id = self.visit(node)
            return self.s_t.find_variable(id, lineno=lineno)[1]
        else:
            return self.visit(node)
