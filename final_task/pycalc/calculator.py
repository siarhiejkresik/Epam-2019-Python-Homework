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


class LeftParen(Symbol):
    lbp = 170

    def prefix(self):
        expr = expression()
        print('left parent prefix, expr from right:', expr)
        print(token)
        advance(RightParen)
        return expr

    # def infix(self, left):
    #     return left ** expression(self.lbp)


class RightParen(Symbol):
    # lbp = 0

    # def prefix(self):
    #     raise Exception('expression cant start with )')

    def infix(self, left):
        return expression(self.lbp)


class Function(Symbol):
    lbp = 160

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
    # lbp = 0

    def prefix(self):
        expr = expression(self.lbp)
        return expr


class End(Symbol):
    # lbp = 0
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
    program = '( 4 ** 3 ) ** 2'
    print(eval(program))
    print(parse(program))
