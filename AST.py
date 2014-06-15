from SymbolTable import *


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


class Input(Node):
    def __init__(self, expr_list):
        self.expr_list = expr_list

    def __str__(self):
        return self.expr_list.__str__()


class Expression(Node):
    def __init__(self, function_name, args):
        self.function_name = function_name
        self.args = args
        self.return_value = None 

    def __str__(self):
        return self.return_value.__str__()

    def getval(self):
        return self.return_value

class ArgList(Node):
    def __init__(self):
        self.args = []

    def add_argument(self,arg):
        self.args.append(arg)

class Arg(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__str__()

    def getval(self):
        return self.value.getval()

class List(Node):
    def __init__(self):
        self.type = "List"
        self.arguments = []

    def add_argument(self,argument):
        self.arguments.append(argument)

    def add_argument_list(self,argument_list):
        self.arguments.extend(argument_list)

    def __str__(self):
        if(len(self.arguments) == 1):
            return "(" + self.arguments[0].__str__() + ")"
        res = "("
        res += reduce((lambda x,y: x.__str__() + " " + y.__str__()), self.arguments)
        return res + ")"

    def getval(self):
        return map(lambda x: x.getval(), self.arguments)

class Atom(Node):
    def __init__(self, value):
        self.value = value
        self.idRetval = None

    def __str__(self):
        if(self.idRetval == None):
            return self.value.__str__()
        return self.idRetval.__str__()

    def getval(self):
        return self.value

class IdName(Node):
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name.__str__()

class Const(Node):
    def __init__(self,value):
        self.type = "Const"
        if type(value) == str:
            self.value = value[1:-1]
        else:
            self.value = value
    def __str__(self):
        return self.value.__str__()

    def getval(self):
        return self.value

class Function(Node):

    def __init__(self, fun_name, args_list, instr_list):
        self.return_type = None
        self.fun_name = fun_name
        self.args_list = args_list.arguments    #List.arguments
        self.instr_list = instr_list            #Expressions or/and Args

        self.symbol_table = SymbolTable(None,"function " + self.fun_name)
        
        if self.args_list:
            for arg in self.args_list:
                arg.set_symbol_table(self.symbol_table)

        map(lambda x: x.set_symbol_table(self.symbol_table), self.instr_list)

    def set_symbol_table_parent(self,parent):
        self.symbol_table.parent = parent

    def __str__(self):
        return self.fun_name

class WhileInstr(Expression):

    def __init__(self,condition,instructions):
        self.condition = condition
        self.instructions = instructions
        self.return_value = None

    def set_symbol_table(self, symbol_table):
        self.symbol_table = symbol_table
        self.condition.set_symbol_table(symbol_table)
        if type(self.instruction) == ArgList:
            self.instruction.set_symbol_table_parent(symbol_table)
        else:
            self.instruction.set_symbol_table(symbol_table)
