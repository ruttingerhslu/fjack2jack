import unittest

from src.jack import JackGenerator

class TestJack(unittest.TestCase):
    def test_parse(self):
        input = ['let', [['t0', ['>', 2, 1]]], ['print', 't0']]
        lifted = []

        expected = "class Main { function void main() { var int t0; let t0 = (2 > 1); do Output.printInt(t0); return; }}"

        gen = JackGenerator()
        jack_code = gen.generate_jack(input, lifted)

        #prepare for comparison
        ast = ' '.join(jack_code.replace("\n", "").split())

        self.assertEqual(ast, expected)
