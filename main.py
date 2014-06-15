
import sys
import ply.yacc as yacc
from LISPparser import LISPparser
from Interpreter import Interpreter


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    LISPparser = LISPparser()
    parser = yacc.yacc(module=LISPparser)
    text = file.read()

    ast = parser.parse(text, lexer=LISPparser.scanner)
    
    ast.accept2(Interpreter())
