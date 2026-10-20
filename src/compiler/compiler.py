import re

TOKEN_TYPES = [
    ('START', r'START\b'),
    ('END', r'END\b'),
    ('ACTION', r'MoveL\b|SET\b'),
    ('BOOLEAN', r'True\b|False\b'),
    ('COORDS', r'\(\s*[-+]?\d*\.?\d+\s*,\s*[-+]?\d*\.?\d+\s*,\s*[-+]?\d*\.?\d+\s*\)'),
    ('NUMBER', r'[-+]?\d*\.?\d+'),
    ('SEPARATOR', r','),
    ('DELIMITER', r';'),
    ('SKIP', r'[ \t\n]+'),
    ('MISMATCH', r'.')
]

def lexer(main_code):
    tokens = []
    regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_TYPES)
    for match_object in re.finditer(regex, main_code):
        kind = match_object.lastgroup
        value = match_object.group()
        if kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Unknown character {value}')
        else:
            if kind == 'NUMBER':
                value = float(value)
            elif kind == 'COORDS':
                cleaned = value.strip('()')
                x_str, y_str, phi_str = cleaned.split(',')
                value = (float(x_str.strip()), float(y_str.strip()), float(phi_str.strip()))
            tokens.append((kind, value))
    return tokens

class CompilerError(Exception):
    def __init__(self, message, token=None):
        self.message = message
        self.token = token
        super().__init__(message)    

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def error(self, message):
        raise CompilerError(message, token=self.actual())

    def actual(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def consume(self, expected_type):
        token = self.actual()
        if token and token[0] == expected_type:
            self.pos += 1
            return token[1]
        found = token[1] if token else "EOF"
        self.error(f"Expected {expected_type}, "f"but found '{found}'")

    def compile(self):
        ast = []
        self.consume('START')
        while self.pos < len(self.tokens) and self.actual()[0] != 'END':
            ast.append(self.parse_instruction())
        self.consume('END')
        return ast

    def parse_instruction(self):
        action = self.consume('ACTION')

        if action == 'MoveL':
            coords = self.consume('COORDS')
            self.consume('SEPARATOR')
            speed = self.consume('NUMBER')
            node = {'action': action, 'coords': coords, 'speed': speed}
        elif action == 'SET':
            state = self.consume('BOOLEAN')
            node = {'action': action, 'value': state}
        else:
            self.error(f"Unknown action '{action}'")
        self.consume('DELIMITER')

        return node

def compile_code(code):
    tokens = lexer(code)
    parser = Parser(tokens)
    return parser.compile()
