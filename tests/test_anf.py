import unittest

from src.fjack import parse
from src.anf import normalize_term

class TestANF(unittest.TestCase):
    def test_lambda(self):
        input = parse("((lambda (x) (> x 1)) 2)")

        expected = [['lambda', ['x'], ['>', 'x', 1]], 2]

        anf = normalize_term(input)

        self.assertEqual(anf, expected)

    def test_named_lambda(self):
        input = ["print", ["let", ["square", ["lambda", ["x"], ["*", "x", "x"]]], ["square", ["+", 1, 2]]]]

        expected = ['let', [['square', ['lambda', ['x'], ['*', 'x', 'x']]]], ['let', [['t0', ['+', 1, 2]]], ['let', [['t1', ['square', 't0']]], ['print', 't1']]]]

        ast = normalize_term(input)

        self.assertEqual(ast, expected)
