from .evaluator import SetStatement, TimesStatement, TimeStatement
from .scanner import TokenType, Scanner

# Grammar rules:
# set_stmt -> "set" stmt *("and" stmt)
# stmt -> times_stmt | time_stmt
# times_stmt -> attribute "to" NUMBER "times"
# time_stmt -> "time" "to" NUMBER
# attribute -> STRING *("," attribute)

class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        try:
            tree = self.set_stmt()
            return tree
        except Exception as e:
            print(e)
            return e

    # set_stmt -> "set" stmt *("and" stmt)
    def set_stmt(self):
        if not self.match(TokenType.SET):
            raise Exception("Expected 'set' in statement.")

        root = SetStatement(self.stmt(), None)
        statement = root
        # command chaining
        while self.match(TokenType.AND):
            and_stmt = self.stmt()
            statement.and_stmt = and_stmt
            statement = statement.and_stmt

        return root

    # stmt -> times_stmt | time_stmt
    def stmt(self):
        if self.peek().token_type == TokenType.STRING:
            return self.times_stmt()
        elif self.peek().token_type == TokenType.TIME:
            return self.time_stmt()

    # times_stmt -> attribute "to" NUMBER "times"
    def times_stmt(self):
        attributes = []
        # attribute -> NUMBER *("," attribute)
        while self.match(TokenType.STRING):
            attributes.append(self.previous().literal)
            if self.match(TokenType.COMMA):
                continue
        
        self.check(TokenType.TO, "Expected 'to' after setting order numbers.")
        times = None
        if self.match(TokenType.NUMBER):
            times = self.previous().literal
        else:
            raise Exception("Expected integer value for number of times to farm the order.")
        self.check(TokenType.TIMES, "Expected 'times' keyword after integer count for number of times to farm the order.")

        return TimesStatement(attributes, times)

    # time_stmt -> "time" "to" NUMBER
    def time_stmt(self):
        self.check(TokenType.TIME, "Expected 'time' keyword to start setting a new time for cooping.")
        self.check(TokenType.TO, "Expected 'to' after 'time' keyword.")

        time = None
        if self.match(TokenType.NUMBER):
            time = self.previous().literal
        else:
            raise Exception("Expected integer value in 24-hour format.")
        return TimeStatement(time)

        

    def match(self, token_type):
        if self.current < len(self.tokens) and self.tokens[self.current].token_type == token_type:
            self.current += 1
            return True
        return False

    def peek(self):
        return self.tokens[self.current]

    def previous(self):
        return self.tokens[self.current - 1]

    def check(self, token_type, msg):
        if not self.match(token_type):
            raise Exception(msg)

    def end(self):
        return self.current >= len(self.tokens)


if __name__ == "__main__":
    command = "set a,b to 2 times"
    scanner = Scanner(command)
    tokens = scanner.scan()
    parser = Parser(tokens)
    statement = parser.parse()