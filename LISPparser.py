
from scanner import Scanner
from AST import *



class LISPparser(object):

    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens


    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print('At end of input')
        exit()

    
    def p_input(self, p):
        """input : expr_list"""
        p[0] = Input(p[1])
    
    def p_expr_list(self, p):
        """expr_list : expr_list expression
                    | expression"""
        if (len(p) == 3 and p[2] != None):
            p[1].append(p[2])
            p[0] = p[1]    
        else:
            p[0] = [p[1]]
    
    def p_expression(self, p):
        """expression : '(' ID expr_list ')'   
                        | '(' DEFUN ID list expr_list ')' 
                        | '(' LOOP expression expr_list ')'
                        | atom"""
        if(len(p) == 2):
            p[0] = p[1]
        elif(len(p) == 5):
            p[0] = Expression(p[2], p[3])
        elif(len(p) == 6):
            p[0] = WhileInstr(p[3], p[4])
        else:
            p[0] = Function(p[3], p[4], p[5])
        # p[0].set_lineno(self.scanner.lineno)

    def p_atom(self, p):
        """atom : INTEGER
                 | FLOAT
                 | STRING
                 | BRACKET expr_list ')'
                 | idname"""
        if(len(p) == 4):
            p[0] = List()
            p[0].add_argument_list(p[2])
        else:    
            p[0] = Atom(p[1])
        # p[0].set_lineno(self.scanner.lineno)

    def p_idname(self, p):
        """idname : ID"""
        p[0] = IdName(p[1])
        # p[0].set_lineno(self.scanner.lineno)

    def p_list(self, p):
        """list : '(' ')' 
                 | '(' expr_list '.' expression ')'
                 | '(' expr_list ')' """
        p[0] = List()
        if(len(p) == 3):
            p[0].add_argument(p[2])
        elif(len(p) == 4):
            p[0].add_argument_list(p[2])
        else:
            p[2].add_argument(p[4])
            p[0].add_argument_list(p[2])
        # p[0].set_lineno(self.scanner.lineno)
