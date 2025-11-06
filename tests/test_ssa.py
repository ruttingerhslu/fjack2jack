import unittest

from src.fjack import *
from src.ssa import *

class TestSSA(unittest.TestCase):
    """
        (lambda_proc (x y k) (k (+ x y))) to
    """
    def test_lambda(self):
        input = ['lambda_proc', ['x', 'y', 'k'], ['k', ['+', 'x', 'y']]]
        ssa_ast = g_proc(input)

        expected = ['proc', ['x', 'y'], ['return', ['x', '+', 'y'], ';']]

        self.assertEqual(ssa_ast, expected)

    def test_if(self):
        input = ['lambda_proc', ['x', 'k'], ['if', ['>', 'x', 0], ['k', ['+', 'x', 1]], ['k', ['-', 'x', 1]]]]
        ssa_ast = g_proc(input)

        expected = ['proc', ['x'], ['if', ['>', 'x', 0], 'then', ['return', ['x', '+', 1], ';'], 'else', ['return', ['x', '-', 1], ';']]]

        self.assertEqual(ssa_ast, expected)

    def test_multiple_labels(self):
        input = ['lambda_proc', ['f', 'limit', 'k'], ['letrec', [['l', ['lambda_jump', ['i', 'c'], ['if', ['=', 'i', 'limit'], ['k', 'c'], ['f', 'i', ['lambda_cont', ['x'], ['letrec', [['j', ['lambda_jump', ["c'"], ['l', ['+', 'i', 1], "c'"]]]], ['if', ['=', 'x', 0], ['j', ['+', 'c', 1]], ['j', 'c']]]]]]]]], ['l', 0, 0]]]
        collect_phi_assignments(input)
        ssa_ast = g_proc(input)

        expected = ['proc', ['f', 'limit'], ['goto', 'l_1;'], ['l', ':', {'i': ['0', "['i', '+', 1]"], 'c': ['0', "c'"]}, ['if', ['=', 'i', 'limit'], 'then', ['return', 'c', ';'], 'else', ['x', '<-', ['f', ['i']], ';', ['if', ['=', 'x', 0], 'then', ['goto', 'j_2;'], 'else', ['goto', 'j_2;']]]]], ['j', ':', {"c'": ["['c', '+', 1]", 'c']}, ['goto', 'l_1;']]]

        self.assertEqual(ssa_ast, expected)
