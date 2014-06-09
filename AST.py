from SymbolTable import *
from TypeChecker import *

class Node(object):
    def accept(self, visitor):
        className = self.__class__.__name__
        # return visitor.visit_<className>(self)
        meth = getattr(visitor, 'visit_' + className, None)
        if meth!=None:
            return meth(self)

    def accept2(self, visitor):
        return visitor.visit(self)

    def set_symbol_table(self,symbol_table):
        self.symbol_table = symbol_table

    def set_lineno(self,lineno):
        self.lineno = lineno

# Caly program
class Program(Node):
    def __init__(self,declarations,fundefs,instructions):
        self.declarations = declarations
        self.fundefs = fundefs
        self.instructions = instructions

        self.symbol_table = SymbolTable(None, "main")
        for decl in self.declarations.declarations:
            decl.set_symbol_table(self.symbol_table)

        for instr in self.instructions:
            if type(instr) == CompoundInstruction:
                instr.set_symbol_table_parent(self.symbol_table)
            instr.set_symbol_table(self.symbol_table)

        for fundef in self.fundefs:
            fundef.set_symbol_table_parent(self.symbol_table)


# Stale
class Const(Node):
    def __init__(self,value):
        if type(value) == str:
            self.value = value[1:-1]
        else:
            self.value = value
    def __str__(self):
        return self.value.__str__()    

# Wyrazenia ==,!=,<=,>= itd.
class BinExpr(Node):

    def __init__(self,operator,left,right):
        self.type = "BinExpr"
        self.operator = operator
        self.left = left
        self.right = right

    def set_symbol_table(self, symbol_table):
        self.symbol_table = symbol_table
        if type(self.left) == BinExpr or type(self.left) == FunCall:
            self.left.set_symbol_table(symbol_table)
        if type(self.right) == BinExpr or type(self.right) == FunCall:
            self.right.set_symbol_table(symbol_table)


# Lista deklaracji
class DeclarationList(Node):

	def __init__(self):
		self.type = "Declarations"
		self.declarations = []

	def add_declaration(self,declaration):
		self.declarations.append(declaration)

	def add_declaration_list(self,declaration_list):
		self.declarations.extend(declaration_list)


# Pojedyncza deklaracja
class Declaration(Node):

    def __init__(self,left,right):
        self.type = "Declaration"
        self.left = left
        self.right = right

    def set_type(self,type):
        self.type = type


# Definicja funkcji
class Function(Node):

    def __init__(self,return_type,fun_name,args_list,instr_list):
        self.return_type = return_type
        self.fun_name = fun_name
        self.args_list = args_list
        self.instr_list = instr_list

        self.symbol_table = SymbolTable(None,"function " + self.fun_name)
        
        if self.args_list:
            for arg in self.args_list:
                arg.set_symbol_table(self.symbol_table)
              
        self.instr_list.set_symbol_table_parent(self.symbol_table)

        TypeChecker.return_type = return_type

    def set_symbol_table_parent(self,parent):
        self.symbol_table.parent = parent


# Argument funkcji
class Arg(Node):

    def __init__(self,type,name):
        self.type = type
        self.name = name


# Klasa bazowa dla instrukcji
class Instruction(Node):
    pass


# Przypisanie
class Assignment(Instruction):
    def __init__(self,left,right):
        self.left = left
        self.right = right  

    def set_symbol_table(self, symbol_table):
        self.symbol_table = symbol_table
        if type (self.right) == BinExpr or type(self.right) == FunCall:
            self.right.set_symbol_table(symbol_table) 



# Instrukcje PRINT, RETURN, BREAK, CONTINUE
class OneArgInstruction(Instruction):

    def __init__(self,name,arg):
        self.name = name.upper()
        self.arg = arg

    def set_function(self,function):
        self.function = function

    def set_symbol_table(self, symbol_table):
        self.symbol_table = symbol_table
        if type(self.arg) == BinExpr or type(self.arg) == FunCall:
            self.arg.set_symbol_table(symbol_table)

# Instrukcja w nawiasach klamrowych 
class CompoundInstruction(Instruction):

    def __init__(self,declarations,instructions):
        self.declarations = declarations
        self.instructions = instructions

        self.symbol_table = SymbolTable(None, "compound")
        for decl in self.declarations.declarations:
            decl.set_symbol_table(self.symbol_table)

        for instr in self.instructions:
            if (type(instr) == CompoundInstruction):
                instr.set_symbol_table_parent(self.symbol_table)
            else:
                instr.set_symbol_table(self.symbol_table)

    def set_symbol_table_parent(self,parent):
        self.symbol_table.parent = parent


# Etykieta
class LabeledInstruction(Instruction):

    def __init__(self,name,instruction):
        self.name = name
        self.instruction = instruction

    def set_symbol_table(self,symbol_table):
        self.instruction.symbol_table = symbol_table


# Instrukcja IF ... ELSE
class Condition(Instruction):

    def __init__(self,condition,instruction,else_instruction):
        self.condition = condition
        self.instruction = instruction
        self.else_instruction = else_instruction

    def set_symbol_table(self, symbol_table):
        self.symbol_table = symbol_table
        self.condition.set_symbol_table(symbol_table)
        if type(self.instruction) == CompoundInstruction:
            self.instruction.set_symbol_table_parent(symbol_table)
        else:
            self.instruction.set_symbol_table(symbol_table)
        if type(self.else_instruction) == CompoundInstruction:
            self.else_instruction.set_symbol_table_parent(symbol_table)
        elif self.else_instruction:
            self.else_instruction.set_symbol_table(symbol_table)


# Instrukcja WHILE
class WhileInstr(Instruction):

    def __init__(self,condition,instruction):
        self.condition = condition
        self.instruction = instruction

    def set_symbol_table(self, symbol_table):
        self.symbol_table = symbol_table
        self.condition.set_symbol_table(symbol_table)
        if type(self.instruction) == CompoundInstruction:
            self.instruction.set_symbol_table_parent(symbol_table)
        else:
            self.instruction.set_symbol_table(symbol_table)
      

# Instrukcja REPEAT ... UNTIL
class RepeatUntilInstr(Instruction):

    def __init__(self,condition,instructions):
        self.condition = condition
        self.instructions = instructions

    def set_symbol_table(self, symbol_table):
        self.symbol_table = symbol_table
        self.condition.set_symbol_table(symbol_table)
        for instr in self.instructions:
            if type(instr) == CompoundInstruction:
                instr.set_symbol_table_parent(symbol_table)
            else:
                instr.set_symbol_table(symbol_table)


# Wywolanie funkcji
class FunCall(Node):

    def __init__(self,fun_name,expr_list):
        self.fun_name = fun_name
        self.expr_list = expr_list

    def set_symbol_table(self, symbol_table):
        self.symbol_table = symbol_table
        for expr in self.expr_list:
            if type(expr) == BinExpr or type(expr) == FunCall:
                expr.set_symbol_table(symbol_table)
        

