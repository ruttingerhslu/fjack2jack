import unittest

from src.beta_reduction import beta_reduce

class TestBetaReduction(unittest.TestCase):
    def test_lambda(self):
        input = [['lambda', ['x'], ['>', 'x', 1]], 2]

        expected = ['>', 2, 1]

        ast = beta_reduce(input)

        self.assertEqual(ast, expected)
