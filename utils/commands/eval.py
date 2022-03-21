class ExprVisitor():
    def visit_literal(literal):
        return literal.value

class StmtVisitor():
    def visit_set_stmt(set_stmt):
        pass


class Literal():
    def __init__(self, value):
        self.value = value

    def accept(self, visitor):
        return visitor.visit_literal(self)

class SetStatement():
    def __init__(self, attribute, expression):
        super().__init__()
        self.attribute = attribute
        self.expression = expression

    def accept(self, visitor):
        return visitor.visit_set_stmt(self)