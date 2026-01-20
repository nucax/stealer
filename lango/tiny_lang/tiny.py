import sys

# ---------------- LEXER ----------------
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def next_token(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

        if self.pos >= len(self.text):
            return None

        c = self.text[self.pos]

        if c.isdigit():
            num = ""
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                num += self.text[self.pos]
                self.pos += 1
            return ("NUMBER", int(num))

        if self.text.startswith("input", self.pos):
            self.pos += 5
            return ("INPUT", None)

        self.pos += 1

        return {
            '+': ("PLUS", None),
            '-': ("MINUS", None),
            '*': ("STAR", None),
            '/': ("SLASH", None),
            '(': ("LPAREN", None),
            ')': ("RPAREN", None),
        }.get(c, ("UNKNOWN", c))


# ---------------- PARSER / EVALUATOR ----------------
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = self.lexer.next_token()

    def eat(self, kind):
        if self.token and self.token[0] == kind:
            self.token = self.lexer.next_token()
        else:
            raise SyntaxError(f"Expected {kind}, got {self.token}")

    def factor(self):
        if self.token[0] == "NUMBER":
            val = self.token[1]
            self.eat("NUMBER")
            return val

        if self.token[0] == "INPUT":
            self.eat("INPUT")
            return int(input("> "))

        if self.token[0] == "LPAREN":
            self.eat("LPAREN")
            val = self.expr()
            self.eat("RPAREN")
            return val

        raise SyntaxError("Invalid expression")

    def term(self):
        val = self.factor()
        while self.token and self.token[0] in ("STAR", "SLASH"):
            if self.token[0] == "STAR":
                self.eat("STAR")
                val *= self.factor()
            else:
                self.eat("SLASH")
                val //= self.factor()
        return val

    def expr(self):
        val = self.term()
        while self.token and self.token[0] in ("PLUS", "MINUS"):
            if self.token[0] == "PLUS":
                self.eat("PLUS")
                val += self.term()
            else:
                self.eat("MINUS")
                val -= self.term()
        return val


# ---------------- RUNNER ----------------
def run(code):
    for line in code.splitlines():
        line = line.strip()
        if not line:
            continue

        if not line.startswith("print"):
            raise SyntaxError("Only 'print' statements are allowed")

        expr = line[5:].strip()
        parser = Parser(Lexer(expr))
        print(parser.expr())


if __name__ == "__main__":
    run(sys.stdin.read())
