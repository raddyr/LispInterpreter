
import ply.lex as lex


class Scanner(object):


  def find_tok_column(self, token):
      last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
      if last_cr < 0:
        last_cr = 0
      return token.lexpos - last_cr


  def build(self):
      self.lexer = lex.lex(object=self)

  def input(self, text):
      self.lexer.input(text)

  def token(self):
      return self.lexer.token()



  literals = "{}()<>=;:,+-*/%&|^"


  reserved = {
    # 'and'     : 'AND',
    # 'or'      : 'OR',
    # 'eq'      : 'EQ',
    # 'not'     : 'NOT',
    # 'car'     : 'CAR',
    # 'cdr'     : 'CDR',
    # 'setq'    : 'SETQ',
    # 'length'  : 'LENGTH',
    # 'print'   : 'PRINT',
    # 'cond'    : 'COND',
    'quote'   : 'QUOTE'
  }


  tokens = [ "FLOAT", "ID", "INTEGER", "STRING", "FUNCTION"
           ] + list(reserved.values())
           

  t_ignore = ' \t\f'
  lineno = 1

  def t_newline(self,t):
      r'\n+'
      t.lexer.lineno += len(t.value)
      self.lineno = t.lexer.lineno

  def t_newline2(self,t):
      r'(\r\n)+'
      t.lexer.lineno += len(t.value) / 2
      self.lineno = t.lexer.lineno


  def t_error(self,t):
      print("Illegal character '{0}' ({1}) in line {2}".format(t.value[0], hex(ord(t.value[0])), t.lexer.lineno))
      t.lexer.skip(1)


  def t_FLOAT(self,t):
      r"\d+(\.\d*)|\.\d+"
      t.value = float(t.value)
      return t

  def t_INTEGER(self,t):
      r"\d+"
      t.value = int(t.value)
      return t
  
  def t_STRING(self,t):
      r'\"([^\\\n]|(\\.))*?\"'
      return t
  
  def t_FUNCTION(self, t):
      r'(\+|-|\*|/|<|<=|>|>=|car|cdr|eq|not|and|or|setq|length|print|do)?\s'
      return t

  def t_ID(self,t):
      r"[a-zA-Z_]+"
      t.type = Scanner.reserved.get(t.value, 'ID')
      return t

  def t_COMMENT(self, t):
    r'[;][^\n]*'
    t.lexer.lineno += t.value.count('\n')
    self.lineno = t.lexer.lineno
