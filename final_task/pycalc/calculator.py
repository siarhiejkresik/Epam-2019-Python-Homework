# import pycalc.packA
# import pycalc.packB
# import Tokens from pycalc.scaner


class Symbol():
    lbp = 0

    def __init__(self, parser):
        self._parser = parser

    def prefix(self):
        raise SyntaxError(f'{self.parser.token} can’t start an expression')

    def infix(self):
        raise SyntaxError()

    def expression(self, *args):
        """Envoke the expression method of a parser."""
        return self._parser.expression(*args)

    def advance(self, *args, **kwargs):
        """Envoke the advance method of a parser."""
        self._parser.advance(*args, **kwargs)

    def is_instance_next_token(self, token_class):
        """Return `True` if the next token is instance of `token_class` class."""
        return self._parser.next_token.is_instance(token_class)

    def is_instance(self, token_class):
        """Return `True` if this token is instance of `token_class`."""
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
        self.advance(RightParen)
        return expr


class RightParen(Symbol):

    def infix(self, left):
        return self.expression(self.lbp)


class Function(Symbol):
    lbp = 160

    def __init__(self, parser, fn=None):
        super().__init__(parser)
        self.fn = fn

    def prefix(self):
        self.advance(LeftParen)

        args = []
        if not self.is_instance_next_token(RightParen):
            while True:
                args.append(self.expression())
                if not self.is_instance_next_token(Comma):
                    break
                self.advance(Comma)
        print('arguments:', args)

        self.advance(RightParen)
        if self.fn:
            return self.fn(args)
        return sum(args)


class Comma(Symbol):
    def prefix(self):
        expr = self.expression(self.lbp)
        return expr


class End(Symbol):
    pass


class Parser:
    def __init__(self):
        self.source = None

        self.token = None
        self.next_token = None

    def parse(self, source):
        if not source:
            raise Exception('can’t parse nothing')
        self.source = source
        self.tokens = tokenize(source, self)

        self.next()
        return self.expression()

    def next(self):
        self.token = self.next_token
        self.next_token = next(self.tokens)

    def advance(self, token_class=None):
        if token_class and not self.next_token.is_instance(token_class):
            raise SyntaxError(f"Expected: {token_class.__name__}")
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
    # program = '- - - 2 ** fn ( 1 , ( 2 + 1 ) * 5 , 4 )'
    # print(eval(program))
    # print(program)
    p = Parser()
    assert p.parse('- - - 2 ** fn ( 1 , ( 2 + 1 ) * 5 , 4 )') == -1048576
    assert p.parse('- - 2') == 2
    assert p.parse('4 ** 3 ** 2') == 262144
    assert p.parse('1 + 2 * 3') == 7
    assert p.parse('( 1 + 2 ) * 3') == 9
    assert p.parse('1 + 2 == 3') is True
    assert p.parse('0 == 1') is False
    # TODO:
    # assert p.parse('0 1') is False
