# import pycalc.packA
# import pycalc.packB
# import Tokens from pycalc.scaner


# def advance(token_class=None):
#     global token
#     if token_class and not token.is_instance(token_class):
#         raise Exception("Syntax error. Expected: " + token_class.__name__)
#     token = next()
#     return


class Symbol(object):
    lbp = 0

    def __init__(self, parser):
        self.parser = parser

    def prefix(self):
        raise NotImplementedError()

    def infix(self):
        raise NotImplementedError()

    def expression(self, *args):
        return self.parser.expression(*args)

    def is_instance(self, token_class):
        return isinstance(self, token_class)

    def __repr__(self):
        return self.__class__.__name__


class Number(Symbol):
    def __init__(self, parser, value):
        super().__init__(parser)
        self.value = int(value)

    def prefix(self):
        return self.value


class Add(Symbol):
    lbp = 110

    def prefix(self):
        right = self.expression(130)
        return right

    def infix(self, left):
        right = self.expression(self.lbp)
        return left + right


class Sub(Symbol):
    lbp = 110

    def prefix(self):
        right = self.expression(130)
        return -right

    def infix(self, left):
        right = self.expression(self.lbp)
        return left - right


class Mul(Symbol):
    lbp = 120

    def infix(self, left):
        return left * self.expression(self.lbp)


class Pow(Symbol):
    lbp = 140

    def infix(self, left):
        return left ** self.expression(self.lbp - 1)


class Eq(Symbol):
    lbp = 60

    def infix(self, left):
        return left == self.expression(self.lbp)


class LeftParen(Symbol):
    # lbp = 170

    def prefix(self):
        expr = self.expression()
        self.parser.advance(RightParen)
        return expr


class RightParen(Symbol):

    def infix(self, left):
        return self.expression(self.lbp)


class Function(Symbol):
    lbp = 160

    def prefix(self):
        self.parser.advance(LeftParen)
        print('in fn:', self.parser.token)
        args = []
        if not self.parser.next_token.is_instance(RightParen):
            while True:
                args.append(self.expression())
                if not self.parser.next_token.is_instance(Comma):
                    break
                self.parser.advance(Comma)
        print('arguments:', args)

        self.parser.advance(RightParen)
        return sum(args)


class Comma(Symbol):
    def prefix(self):
        expr = self.expression(self.lbp)
        return expr


class End(Symbol):
    pass


class Parser:
    def __init__(self, source):
        self.source = source
        self.tokens = tokenize(source, self)

        self.token = None
        self.next_token = None

    def parse(self):
        self.next()
        return self.expression()

    def next(self):
        self.token = self.next_token
        self.next_token = next(self.tokens)

    def advance(self, token_class=None):
        if token_class and not self.next_token.is_instance(token_class):
            raise Exception("Syntax error. Expected: " + token_class.__name__)
        self.next_token = next(self.tokens)

    def expression(self, rbp=0):
        self.next()
        left = self.token.prefix()
        print('in expression start:', self.token, self.next_token, left)
        while rbp < self.next_token.lbp:
            self.next()
            # print('t    :', t)
            # print('token:', token)
            # print('rbp  :', rbp)
            left = self.token.infix(left)

        return left


def tokenize(source, parser):
    tokens = source.split()
    for literal in tokens:
        print('literal:',  literal)
        if literal.isdigit():
            yield Number(parser, literal)
        elif literal == "+":
            yield Add(parser)
        elif literal == "-":
            yield Sub(parser)
        elif literal == "*":
            yield Mul(parser)
        elif literal == "**":
            yield Pow(parser)
        elif literal == "(":
            yield LeftParen(parser)
        elif literal == ")":
            yield RightParen(parser)
        elif literal == "fn":
            yield Function(parser)
        elif literal == ",":
            yield Comma(parser)
        elif literal == "==":
            yield Eq(parser)
        else:
            raise SyntaxError('unknown operator: %s', literal)
    yield End(parser)


def run(expression):
    result = 40
    # print(f'running calc.py calculate({expression})...')
    print(result)
    return result


if __name__ == "__main__":
    program = 'fn ( 1 , 2 , 4 )'
    # print(eval(program))
    p = Parser(program)
    print(p.parse())
