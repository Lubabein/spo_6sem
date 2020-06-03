from token import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.expressions = []

    def lang(self):
        flag = True
        while self.pos < len(self.tokens):
            flag, pos = self.expr(self.pos)
            if not flag:
                print('error')
                break
        return flag

    def expr(self, num):
        expr, new_pos = self.assign_expr(num)
        expr_if, new_pos_if = self.if_expr(num)
        expr_while, new_pos_while = self.while_expr(num)
        self.pos = new_pos_if + new_pos + new_pos_while
        return expr or expr_if or expr_while,  self.pos


    def if_expr(self, num):
        if len(self.tokens) - num < 7 or not self.if_t(num):
            return False, 0
        if_expr, num = self.head(num+1)
        if_ex, num = self.body(num)
        if_el = True
        num+=1
        if self.else_t(num):
            if_el, num = self.body(num+1)
        return if_expr and if_ex and if_el, num+1

    def while_expr(self, num):
        if len(self.tokens) - num < 7 or not self.while_t(num):
            return False, 0
        while_expr, num = self.head(num+1)
        while_ex, num = self.body(num)
        return while_expr and while_ex, num + 1

    def body(self, num):
        body = self.ob(num)
        num+=1
        while num <= len(self.tokens) :
           if self.cb(num):
               return body, num
           body, num = self.expr(num)
           if not body:
               return False, 0
        return body, num

    def head(self, num):
        return self.op(num) and self.log_expr(num+1) and self.cp(num+4), num+5

    def log_expr(self, n):
        return self.value(n) and self.log_op(n+1) and self.value(n+2)

    def assign_expr(self, num):
        var = self.var(num)
        assign = self.assign(num + 1)
        if not (var and assign):
            return False, 0
        value_expr, new_pos = self.value_expr(num + 2)
        if var and assign and value_expr:
            return True,  2 + new_pos
        else:
            return False, 0

    def value_expr(self, n):
        op_c = 0
        cp_c = 0
        val2 = True
        while (not self.semicolon(n)):
            if self.cp(n):
                cp_c += 1
            if self.op(n):
                op_c += 1
            val2 = val2 and (self.value(n) or self.ari_oper(n) or self.cp(n) or self.op(n))
            n += 1
            if not val2:
                return False, 0
        if op_c != cp_c:
            return False, 0
        return val2, n-1

    def value(self, num):
        return self.var(num) or self.digit(num)

    def semicolon(self, num):
        return self.find_token(self.tokens[num].get_type(), 'SEMICOLON')

    def var(self, num):
        return self.find_token(self.tokens[num].get_type(), 'VAR')

    def assign(self, num):
        return self.find_token(self.tokens[num].get_type(), 'ASSIGN_OP')

    def digit(self, num):
        return self.find_token(self.tokens[num].get_type(), 'DIGIT')

    def ari_oper(self, num):
        return self.find_token(self.tokens[num].get_type(), 'ARI_OP')

    def op(self, num):
        return self.find_token(self.tokens[num].get_type(), 'OP')

    def cp(self, num):
        return self.find_token(self.tokens[num].get_type(), 'CP')

    def if_t(self, num):
        return self.find_token(self.tokens[num].get_type(), 'IF')

    def while_t(self, num):
        return self.find_token(self.tokens[num].get_type(), 'WHILE')

    def else_t(self, num):
        return self.find_token(self.tokens[num].get_type(), 'ELSE')

    def ob(self, num):
        return self.find_token(self.tokens[num].get_type(), 'OB')

    def cb(self, num):
        return self.find_token(self.tokens[num].get_type(), 'CB')

    def log_op(self, num):
        return self.find_token(self.tokens[num].get_type(), 'LOG_OP')

    def find_token(self, type, found_t):
        if type == found_t:
            #print('Найдено', type)
            return True
        else:
            #print('упс', type,'искали -', found_t)
            return False