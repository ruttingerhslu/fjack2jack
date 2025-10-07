# fjack2jack
FJack to Jack transpiler

## FJack
FJack is a functional language based on Jack, the programming language implemented in Nand2Tetris.

As an example, we want to parse the following line of code:
```fun x -> x * 2```

First, we want to tokenize the input to use them afterwards.
```
[
    FUN,
    IDENTIFIER("x"),
    ARROW,
    IDENTIFIER("x"),
    ASTERISK,
    INTEGER(2),
    SEMICOLON
]
```

Then, we take those tokens and parse them into an abstract syntax tree.

## Testing
To test this project run:
```
pytest
```
