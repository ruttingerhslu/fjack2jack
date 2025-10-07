# fjack2jack
FJack to Jack transpiler

## FJack
FJack is a functional language based on Jack, the programming language implemented in Nand2Tetris.

As an example, we want to parse the following line of code:
```fun x -> x * 2```

First, we want to tokenize the input to use them afterwards.
```
[
    FUNCTION,
    IDENTIFIER("x"),
    ARROW,
    IDENTIFIER("x"),
    ASTERISK,
    INTEGER(2),
    SEMICOLON
]
```

Then, we take those tokens and parse them into an abstract syntax tree.

## Setup
Use the following command in the root directory to start the REPL:
```
python -m src.__main__
```

To test this project run:
```
pytest
```
