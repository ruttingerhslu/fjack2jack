import unittest

from src.fjack import parse

class TestFJack(unittest.TestCase):
    def test_parse(self):
        input = "((lambda (x) (> x 1)) 2)"

        expected = [['lambda', ['x'], ['>', 'x', 1]], 2]

        ast = parse(input)

        self.assertEqual(ast, expected)
