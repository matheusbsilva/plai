from plai.parser import parse


class TestBasicTokens:
    def test_token_number(self):
        assert parse('7') == 7

    def test_token_string(self):
        assert parse('"hello"') == "hello"

    def test_escaped_token_string(self):
        assert parse(r'"hello \"world\""') == 'hello "world"'
        assert parse(r'"hello \n world"') == "hello \n world"
        assert parse(r'"hello \t world"') == "hello \t world"
