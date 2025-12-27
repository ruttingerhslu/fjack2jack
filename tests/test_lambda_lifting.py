import unittest

from src.lambda_lifting import lambda_lift

class TestLambdaLifting(unittest.TestCase):
    def test_named_lambda(self):
        input = ['let', [['square', ['lambda', ['x'], ['*', 'x', 'x']]]], ['let', [['t0', ['+', 1, 2]]], ['let', [['t1', ['square', 't0']]], ['print', 't1']]]]

        expected_ast = ['let', [['square', 'square']], ['let', [['t0', ['+', 1, 2]]], ['let', [['t1', ['square', 't0']]], ['print', 't1']]]]
        expected_lifted = [['function', 'square', ['x'], ['*', 'x', 'x']]]

        ast, lifted = lambda_lift(input)

        self.assertEqual(ast, expected_ast)
        self.assertEqual(lifted, expected_lifted)
