# import pycalc.packA
# import pycalc.packB
# import Tokens from pycalc.scaner


def advance(token_class=None):
    global token
    # print(token, token_class)
    if token_class and not isinstance(token, token_class):
        raise Exception("Syntax error. Expected: " + token_class.__name__)
    token = next()
    return


class Symbol(object):
    lbp = 0

    def prefix(self):
        raise NotImplementedError()

    def infix(self):
        raise NotImplementedError()

    def __str__(self):
        return self.__class__.__name__


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
        advance(RightParen)
        return expr

    # def infix(self, left):
    #     return left ** expression(80 - 1)


class RightParen(Symbol):
    lbp = 0

    def infix(self, left):
        return left ** expression(80 - 1)


class Function(Symbol):
    lbp = 170

    def prefix(self):
        advance(LeftParen)
        print('in fn:', token)
        args = []
        if not isinstance(token, RightParen):
            while True:
                args.append(expression(0))
                if not isinstance(token, Comma):
                    break
                advance(Comma)
        print('arguments:', args)

        advance(RightParen)
        return sum(args)


class Comma(Symbol):
    lbp = 0

    def prefix(self):
        expr = expression(self.lbp)
        return expr


class End(Symbol):
    lbp = 0


def tokenize(program):
    tokens = program.split()
    print(tokens)
    for literal in tokens:
        print('literal:',  literal)
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
        elif literal == "fn":
            yield Function()
        elif literal == ",":
            yield Comma()
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
    # try:
    global token, next
    next = tokenize(program).next
    token = next()
    return expression()
    # except Exception as e:
    # print(e)


def run(expression):
    result = 40
    # print(f'running calc.py calculate({expression})...')
    print(result)
    return result


if __name__ == "__main__":
    program = 'fn ( )'
    # print(eval(program))
    print(parse(program))
