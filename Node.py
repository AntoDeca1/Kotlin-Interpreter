class Node:
    def __init__(self, type, children=None, leaf=None):
        """
        Generic node of the AST
        :param type: Type of the node (e.g. 'ExpressionNode')
        :param children: List of children nodes (if not empty)
        :param leaf: Exposed value (if present)
        """
        self.node_type = type
        self.children = children if children is not None else []
        self.leaf = leaf

    def add_child(self, child_node):
        self.children.append(child_node)

    def __str__(self, level=0):
        """
        A method useful to show the AST
        How To Use :print(rootNode)
        """
        indent = "  " * level
        result = f"{indent}{self.node_type}"

        if self.leaf is not None:
            result += f": {self.leaf}"

        for child in self.children:
            result += "\n" + child.__str__(level + 1)

        return result
