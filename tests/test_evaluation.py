from plai.interpreter import run


class TestExpressions:
    def test_number_sum_expressions(self):
        assert run('1 + 2') == 3
        assert run('1 + 2 + 3') == 6
