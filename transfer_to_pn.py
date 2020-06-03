from token import Token

def print_tokens(tokens):
    for t in tokens:
        print('''({}: '{}')'''.format(t.get_type(), t.get_value()), end=' ')
    print()

op_priority = {
    '(': 0,
    ')': 1,
    '+': 2,
    '-': 2,
    '*': 3,
    '/': 3,
    '>': -1,
    '<': -1,
    '==': -1,
    '!=': -1,
    '=': -1}

class PN:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = []
        self.output = []
        self.token_count = 0

    def transfer_PN(self):
        while self.token_count < len(self.tokens):
            if self.tokens[self.token_count].get_type()=='IF':
                self.output += self.if_pn()
            elif self.tokens[self.token_count].get_type()=='WHILE':
                self.output += self.while_pn()
            else:
                self.output += self.expr_PN('SEMICOLON')
            self.token_count += 1
        print_tokens(self.output)
        return self.output

    def while_pn(self):
        _output = []
        self.token_count += 2
        _output += self.expr_PN('CP')
        _output.append(Token('GO_F', ''))
        self.token_count += 2
        while self.tokens[self.token_count].get_type() not in 'CB':
            _output += self.expr_PN('SEMICOLON')
            self.token_count += 1
        for o in _output:
            if o.get_type() == 'GO_F':
                o.set_value(len(self.output) + len(_output))
        _output.append(Token('GO_A', ''))
        self.token_count += 1
        for o in _output:
            if o.get_type() == 'GO_A':
                o.set_value(len(self.output)-1)
        return _output
        return _output


    def if_pn(self):
        _output = []
        self.token_count += 2
        _output += self.expr_PN('CP')
        _output.append(Token('GO_F', ''))
        self.token_count += 2
        while self.tokens[self.token_count].get_type() not in 'CB':
            _output += self.expr_PN('SEMICOLON')
            self.token_count += 1
        for o in _output:
            if o.get_type() == 'GO_F':
                o.set_value(len(self.output)+len(_output))
        _output.append(Token('GO_A', ''))
        self.token_count += 1
        if self.tokens[self.token_count].get_type() == 'ELSE':
            self.token_count += 2
            while self.tokens[self.token_count].get_type() not in 'CB':
                _output += self.expr_PN('SEMICOLON')
                self.token_count += 1
        for o in _output:
            if o.get_type() == 'GO_A':
                o.set_value(len(self.output) + len(_output)-1)
        return _output

    def expr_PN(self, stop_token):
        _output = []
        _stack = []
        while self.tokens[self.token_count].get_type() not in stop_token:
            if self.tokens[self.token_count].get_type()=='VAR' or self.tokens[self.token_count].get_type()=='DIGIT':
                _output.append(self.tokens[self.token_count])
            elif self.tokens[self.token_count].get_type()=='OP':
                 _stack.append(self.tokens[self.token_count])

            elif self.tokens[self.token_count].get_type()=='CP':
                while _stack[-1].get_type() != 'OP':
                    _output.append(_stack.pop())
                _stack.pop()
            else:

                if _stack == []:
                    _stack.append(self.tokens[self.token_count])
                else:
                    while get_priority(_stack[-1].get_value()) >= get_priority(self.tokens[self.token_count].get_value()):
                        _output.append(_stack.pop())
                        if _stack==[]:
                            break
                    _stack.append(self.tokens[self.token_count])
            self.token_count += 1
        while not _stack==[]:
            _output.append(_stack.pop())
        return _output


def get_priority(op):
        try:
            priority = op_priority[op]
            return priority
        except KeyError:
            print('error', op)