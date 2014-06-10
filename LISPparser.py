
from scanner import Scanner
from AST import *



class LISPparser(object):


    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens


    # precedence = (
    #    ("nonassoc", 'IFX'),
    #    ("nonassoc", 'ELSE'),
    #    ("right", '='),
    #    ("left", 'OR'),
    #    ("left", 'AND'),
    #    ("left", '|'),
    #    ("left", '^'),
    #    ("left", '&'),
    #    ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
    #    ("left", 'SHL', 'SHR'),
    #    ("left", '+', '-'),
    #    ("left", '*', '/', '%'),
    # )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno, self.scanner.find_tok_column(p), p.type, p.value))
        else:
            print('At end of input')
        exit()

    
    
    def p_input(self, p):
        """input : input line 
                  | """
        pass

    def p_line(self, p):
        """line : expression NEWLINE
                  | NEWLINE """
        pass #TODO: print RESULT
    
    
    def p_expression(self, p):
        """expression : '(' FUNCTION arg_list ')'
                        | atom """
        if(len(p) == 5):
            p[0] = Expression(p[2], p[3])
        elif(len(p) == 2):
            p[0] = Expression(p[1])
        p[0].set_lineno(self.scanner.lineno)
    
    def p_arg_list(self, p):
        """arg_list : arg
                     | arg_list arg """
        pass #p[0].set_lineno(self.scanner.lineno)

    def p_arg(self, p):
        """arg : atom
                | list """
        pass #p[0].set_lineno(self.scanner.lineno)

    def p_atom(self, p):
        """atom : INTEGER
                 | FLOAT
                 | STRING
                 | ID"""
        p[0] = Const(p[1])
        p[0].set_lineno(self.scanner.lineno)

    def p_list(self, p):
        """list : '(' ')' 
                 | '(' arg_list ')'
                 | '(' arg_list '.' arg ')'
                 | '\\'' arg
                 | QUOTE arg """
        pass #p[0].set_lineno(self.scanner.lineno)