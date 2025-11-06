# lispy2jack
A source-to-source compiler from Lispy to Jack.

## Setup
Use the following command in the root directory to start the REPL:
```
python -m src.__main__
```

To test this project run:
```
pytest
```

## Demo
Possible code:
```
(lambda (f limit) (loop l ((i 0) (c 0)) (if (= i limit) c (let ((x (f i))) (let ((c' (if (= x 0) (+ c 1) c))) (l (+ i 1) c'))))))
```

Translated to CPS:
```
['lambda_proc', ['f', 'limit', 'k'], ['letrec', [['l', ['lambda_jump', ['i', 'c'], ['if', ['=', 'i', 'limit'], ['k', 'c'], ['let', [['x', ['f', 'i']]], ['letrec', [['j', ['lambda_jump', ["c'"], ['l', ['+', 'i', 1], "c'"]]]], ['if', ['=', 'x', 0], ['j', ['+', 'c', 1]], ['j', 'c']]]]]]]], ['l', 0, 0]]]
```

Translated to SSA:
```
['proc', ['f', 'limit'], ['goto', 'l_1;'], ['l', ':', {'i': [0, i+1], 'c': [0, c']}, ['if', ['=', 'i', 'limit'], 'then', ['return', 'c', ';'], 'else', ['x', '<-', ['f', 'i'], ';', ['if', ['=', 'x', 0], 'then', ['goto', 'j_2;'], 'else', ['goto', 'j_2;']]]] ['j', ':', {"c'": [c+1, c]}, ['goto', 'l_2', ';']]]]
```
