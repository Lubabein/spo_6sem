from token import Token
def print_tokens(tokens):
    for t in tokens:
        print('''({}: '{}')'''.format(t.get_type(), t.get_value()), end=' ')
    print()

class stack_machine:
    def __init__(self, tokens):
        self.tokens = tokens
        self.stack = []
        self.output = []
        self.value_table = []
        self.token_count = 0

    def stack_machine_run(self):
        while self.token_count < len(self.tokens):
            if self.tokens[self.token_count].get_type() == 'VAR' or self.tokens[self.token_count].get_type() == 'DIGIT':
                self.stack.append(self.tokens[self.token_count])
            elif self.tokens[self.token_count].get_type() == 'ARI_OP':
                    self.stack.append(self.calculate())
            elif self.tokens[self.token_count].get_type() == 'ASSIGN_OP':
                self.assign_op()
            elif self.tokens[self.token_count].get_type() == 'LOG_OP':
                self.stack.append(self.calculate())
            elif self.tokens[self.token_count].get_type() == 'GO_F':
                flag = self.stack.pop().get_value()
                if flag == False:
                    self.token_count = self.tokens[self.token_count].get_value()
            elif self.tokens[self.token_count].get_type() == 'GO_A':
                self.token_count = self.tokens[self.token_count].get_value()
            self.token_count += 1
        print(self.value_table)

    def calculate(self):
        e2 = self.stack.pop()
        e1 = self.stack.pop()
        if e1.get_type() == 'VAR':
            e1 = self.find_value(e1.get_value())
        else:
            e1 = e1.get_value()
        if e2.get_type() == 'VAR':
            e2 = self.find_value(e2.get_value())
        else:
            e2 = e2.get_value()
        return self.operation(e1, e2, self.tokens[self.token_count].get_value())
    
    def assign_op(self):
        e2 = self.stack.pop()
        e1 = self.stack.pop()
        flag = True
        for i in range(len(self.value_table)):
            if e1.get_value() == self.value_table[i][0]:
                flag = False
                self.value_table[i][-1] = e2.get_value()
        if flag:
            self.value_table.append([e1.get_value(),e2.get_value()])



    def operation(self, e1, e2, op):
        if op == '-':
            return Token('DIGIT', float(e1) - float(e2))
        if op == '+':
            return Token('DIGIT', float(e1) + float(e2))
        if op == '*':
            return Token('DIGIT', float(e1) * float(e2))
        if op == '/':
            return Token('DIGIT', round(float(e1) / float(e2), 3))
        if op == '==':
            return Token('BOOL', float(e1) == float(e2))
        if op == '!=':
            return Token('BOOL', float(e1) != float(e2))
        if op == '>':
            return Token('BOOL', float(e1) > float(e2))
        if op == '<':
            return Token('BOOL', float(e1) < float(e2))

    def find_value(self,name):
        for i in range(len(self.value_table)):
            if name == self.value_table[i][0]:
                return self.value_table[i][-1]

