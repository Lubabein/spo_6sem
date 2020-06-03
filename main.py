from lexer import Lexer
from pars import Parser
from transfer_to_pn import PN
from stack_machine import stack_machine

f = open('test1.txt')
inp = f.read()
f.close()

print('\nlexer:')
l = Lexer()
tokens = l.lex(inp)

p = Parser(tokens)
pars = p.lang()
print('\nparser: ', pars)
if pars:
    print('\nPN:')
    pn = PN(tokens)
    transfer = pn.transfer_PN()
    print('\nstack machine:')
    sm = stack_machine(transfer)
    sm.stack_machine_run()


