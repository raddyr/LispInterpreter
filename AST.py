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


class Expression(Node):
    def __init__(self, function_name, args, arg):
        self.function_name = function_name
        self.args = args
        self.arg = arg

class ArgList(Node):
    def __init__(self):
        self.args = []

class Arg(Node):
    def __init__(self, value):
        self.value = value

# Listy
class List(Node):
    def __init__(self):
        self.type = "List"
        self.arguments = []

    def add_argument(self,argument):
        self.arguments.append(argument)

    def add_argument_list(self,argument_list):
        self.arguments.extend(argument_list)

class Atom(Node):
    def __init__(self, name, value): #zmienne
        self.type = "Variable"
        self.name = name
        self.value = value
    def __init__(self, value): #stale
        self.type = "Const"
        self.value = value

# Stale
class Const(Node):
    def __init__(self,value):
        if type(value) == str:
            self.value = value[1:-1]
        else:
            self.value = value
    def __str__(self):
        return self.value.__str__()    
#---------------------------------------------------------
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
class FunArg(Node):

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

# # Instrukcja w nawiasach klamrowych 
# class CompoundInstruction(Instruction):

#     def __init__(self,declarations,instructions):
#         self.declarations = declarations
#         self.instructions = instructions

#         self.symbol_table = SymbolTable(None, "compound")
#         for decl in self.declarations.declarations:
#             decl.set_symbol_table(self.symbol_table)

#         for instr in self.instructions:
#             if (type(instr) == CompoundInstruction):
#                 instr.set_symbol_table_parent(self.symbol_table)
#             else:
#                 instr.set_symbol_table(self.symbol_table)

#     def set_symbol_table_parent(self,parent):
#         self.symbol_table.parent = parent

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
        

