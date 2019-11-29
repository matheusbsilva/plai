from plai.parser import parse
from plai.symbol import Symbol


class TestBasicTokens:
    def test_token_number(self):
        assert parse('7') == 7
        assert parse('8.1') == 8.1

    def test_token_string(self):
        assert parse('"hello"') == "hello"
        assert parse('"hello world"') == "hello world"

    def test_escaped_token_string(self):
        assert parse(r'"hello \"world\""') == 'hello "world"'
        assert parse(r'"hello \n world"') == "hello \n world"
        assert parse(r'"hello \t world"') == "hello \t world"


class TestBasicExp:
    def test_sum(self):
        assert parse('1+2') == [Symbol("+"), 1, 2]

    def test_subtraction(self):
        assert parse('1-2') == [Symbol('-'), 1, 2]

    def test_multiplication(self):
        assert parse('1*2') == [Symbol('*'), 1, 2]

    def test_division(self):
        assert parse('1/2') == [Symbol('/'), 1, 2]
