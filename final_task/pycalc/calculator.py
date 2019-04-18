# import pycalc.packA
# import pycalc.packB
# import Tokens from pycalc.scaner


def advance(literal=None):
    global token
    if literal and isinstance(token, RightParen):
        raise SyntaxError("Expected %r" % literal)
    token = next()


class Symbol():
    lbp = 0

    def prefix(self):
        raise NotImplementedError()

    def infix(self):
        raise NotImplementedError()


class Literal(Symbol):
    def __init__(self, value):
        self.value = int(value)

    def prefix(self):
        return self.value


class Add(Symbol):
    lbp = 10

    def prefix(self):
        return expression(100)

    def infix(self, left):
        right = expression(10)
        return left + right


class Sub(Symbol):
    lbp = 10

    def prefix(self):
        right = expression(100)
        return -right

    def infix(self, left):
        right = expression(10)
        return left - right


class Mul(Symbol):
    lbp = 20

    def infix(self, left):
        return left * expression(self.lbp)


class Pow(Symbol):
    lbp = 80

    def infix(self, left):
        return left ** expression(80 - 1)


class LeftParen(Symbol):
    lbp = 150

    def prefix(self):
        expr = expression(100)
        print(expr)
        advance(')')
        return expr

    # def infix(self, left):
    #     return left ** expression(80 - 1)


class RightParen(Symbol):
    lbp = 0

    def infix(self, left):
        return left ** expression(80 - 1)


class End(Symbol):
    lbp = 0


def tokenize(program):
    for literal in program.split(' '):
        # print literal
        if literal.isdigit():
            yield Literal(literal)
        elif literal == "+":
            yield Add()
        elif literal == "-":
            yield Sub()
        elif literal == "*":
            yield Mul()
        elif literal == "**":
            yield Pow()
        elif literal == "(":
            yield LeftParen()
        elif literal == ")":
            yield RightParen()
        else:
            raise SyntaxError('unknown operator: %s', literal)
    yield End()


def expression(rbp=0):
    global token
    t = token
    token = next()
    left = t.prefix()
    while rbp < token.lbp:
        t = token
        token = next()
        left = t.infix(left)

    return left


def parse(program):
    global token, next
    next = tokenize(program).next
    token = next()
    return expression()


def run(expression):
    result = 40
    # print(f'running calc.py calculate({expression})...')
    print(result)
    return result


if __name__ == "__main__":
    program = '( 10 + 20 )'
    print(eval(program))
    print(parse(program))
