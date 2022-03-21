from enum import Enum

class TokenType(Enum):
    EOF = 0
    SET = 1
    TIMES = 2
    TIME = 3
    TO = 4
    AND = 5
    NUMBER = 6
    COMMA = 7

KEYWORDS = {
    "set": TokenType.SET,
    "times": TokenType.TIMES,
    "time": TokenType.TIME,
    "to": TokenType.TO,
    "and": TokenType.AND,
}

class Token():
    def __init__(self, token_type, lexeme, literal):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal

class Scanner():
    def __init__(self, source):
        self.source = source
        self.current = 0
        self.tokens = []


    def scan(self):
        while not self.end():
            token = self.scan_token()
            if token is None:
                continue
            print(token.lexeme)
            self.tokens.append(token)

        return self.tokens
    
    def scan_token(self):
        def isCharacter(c):
            return (c >= "A"  and c <= "Z") or (c >= "a" and c <= "z")

        def isNumber():
            return self.peek() >= "0" and self.peek() <= "9"
        
        if isCharacter(self.peek()):
            keyword = self.next()
            while not self.end() and isCharacter(self.peek()):
                keyword += self.next()
                if keyword in KEYWORDS.keys():
                    # maximal munch, continue consuming until its not a character anymore (case when 'time' vs 'times' keyword)
                    if not self.end() and isCharacter(self.peek()):
                        continue
                    return Token(KEYWORDS[keyword], keyword, keyword)
            print("keyword", keyword)
            raise Exception("Unidentified keyword!")
        elif isNumber():
            number = self.next()
            while not self.end() and isNumber():
                number += self.next()
            return Token(TokenType.NUMBER, number, int(number))
        elif self.match(","):
            return Token(TokenType.COMMA, ",", ",")
        elif self.match("\n", " "):
            return None

        raise Exception("Unidentified keyword!")
        

    def match(self, *args):
        for char in args:
            if self.peek() == char:
                self.next()
                return True
        return False
        

    def next(self):
        ret = self.peek()
        if self.end():
            return ret
        self.current += 1
        return ret

    def peek(self):
        return self.source[self.current]

    def previous(self):
        if self.current == 0:
            return self.source[0]
        return self.source[self.current - 1]

    def end(self):
        return self.current >= len(self.source)