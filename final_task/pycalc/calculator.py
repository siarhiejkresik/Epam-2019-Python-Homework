# import pycalc.packA
# import pycalc.packB
# import Tokens from pycalc.scaner


def advance(token_class=None):
    global token
    if token_class and not token.is_instance(token_class):
        raise Exception("Syntax error. Expected: " + token_class.__name__)
    token = next()
    return


class Symbol(object):
    lbp = 0

    def prefix(self):
        raise NotImplementedError()

    def infix(self):
        raise NotImplementedError()

    def is_instance(self, token_class):
        return isinstance(self, token_class)

    def __repr__(self):
        return self.__class__.__name__


class Number(Symbol):
    def __init__(self, value):
        self.value = int(value)

    def prefix(self):
        return self.value


class Add(Symbol):
    lbp = 110

    def prefix(self):
        right = expression(130)
        return right

    def infix(self, left):
        right = expression(self.lbp)
        return left + right


class Sub(Symbol):
    lbp = 110

    def prefix(self):
        right = expression(130)
        return -right

    def infix(self, left):
        right = expression(self.lbp)
        return left - right


class Mul(Symbol):
    lbp = 120

    def infix(self, left):
        return left * expression(self.lbp)


class Pow(Symbol):
    lbp = 140

    def infix(self, left):
        return left ** expression(self.lbp - 1)


class Eq(Symbol):
    lbp = 60

    def infix(self, left):
        return left == expression(self.lbp)


class LeftParen(Symbol):
    lbp = 170

    def prefix(self):
        expr = expression()
        advance(RightParen)
        return expr


class RightParen(Symbol):

    def infix(self, left):
        return expression(self.lbp)


class Function(Symbol):
    lbp = 160

    def prefix(self):
        advance(LeftParen)
        print('in fn:', token)
        args = []
        if not token.is_instance(RightParen):
            while True:
                args.append(expression(0))
                if not isinstance(token, Comma):
                    break
                advance(Comma)
        print('arguments:', args)

        advance(RightParen)
        return sum(args)


class Comma(Symbol):
    def prefix(self):
        expr = expression(self.lbp)
        return expr


class End(Symbol):
    pass


def tokenize(program):
    tokens = program.split()
    print(tokens)
    for literal in tokens:
        print('literal:',  literal)
        if literal.isdigit():
            yield Number(literal)
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
        elif literal == "==":
            yield Eq()
        else:
            raise SyntaxError('unknown operator: %s', literal)
    yield End()


def expression(rbp=0):
    global token
    t = token
    token = next()
    left = t.prefix()
    print('in expression start:', t, token, left)
    while rbp < token.lbp:
        t = token
        token = next()
        print('t    :', t)
        print('token:', token)
        print('rbp  :', rbp)
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
    program = '1 == 1'
    # print(eval(program))
    print(parse(program))
