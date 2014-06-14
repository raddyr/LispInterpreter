import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
from BuiltInFunctions import builtIns

class Interpreter(object):

    globalMemory = MemoryStack(Memory("global"))
    functionMemory = MemoryStack(Memory("function"))
    functions = []

    @on('node')
    def visit(self, node):
        pass

    @when(AST.Input)
    def visit(self, node):
        map(lambda x: x.accept2(self), node.expr_list)
        print node.expr_list[-1]


    @when(AST.Expression)
    def visit(self, node):
        # print Interpreter.functions
        map(lambda x: x.accept2(self), node.args)
        function = None
        try:
            if(node.function_name not in builtIns):
                raise FunctionNotFound
            res = builtIns[node.function_name](map(lambda x: Interpreter.evalNode(self, x), node.args))
            node.return_value = res
            return res
            # raise ReturnValueException(node.return_value) #TO TYLKO JESLI BEDZIEMY CHCIELI OBSLUZYC RETURN!
        except FunctionNotFound:
            for func in Interpreter.functions:
                if (func.fun_name == node.function_name):
                    function = func
                    break
            if (function == None):
                return
            Interpreter.functionMemory.push(Memory(node.function_name + "_scope"))
            for i in range(len(function.args_list)):
                value = Interpreter.evalNode(self,node.args[i])
                Interpreter.functionMemory.insert(function.args_list[i].value, value)
            retval = None
            try:
                for i in range(len(function.instr_list)):
                    retval = function.instr_list[i].accept2(self)
            except ReturnValueException as e:
                node.return_value = e.value
                return e.value
            node.return_value = retval
            return retval  
        
    @when(AST.Const)
    def visit(self, node):
        return node.value

    @when(AST.List)
    def visit(self, node):
        #return node.arguments
        return map(lambda x: x.accept2(self), node.arguments)

    @when(AST.Arg)
    def visit(self, node):
        node.value.accept2(self) 
        return node.value

    @when(AST.Atom)
    def visit(self, node):
        return node.value

    @when(AST.ArgList)
    def visit(self, node):
        node.value.accept2(self) 
        return node.value
    
    @when(AST.DeclarationList)
    def visit(self, node):
        for decl in node.declarations:
            decl.accept2(self)

    @when(AST.Declaration)
    def visit(self, node):
        name = node.left
        value = node.right.accept2(self)
        Interpreter.current_scope().insert(name, value)

    @when(AST.Function)
    def visit(self, node):
        Interpreter.functions.append(node)

    @when(AST.Assignment)
    def visit(self, node):
        value = Interpreter.evalNode(self, node.right)

        if Interpreter.current_scope().set(node.left, value) == False:
            Interpreter.globalMemory.set(node.left, value)

    # @when(AST.CompoundInstruction)
    # def visit(self, node):
    #     Interpreter.current_scope().push(Memory("compound_instruction"))
    #     node.declarations.accept2(self)
    #     for instr in node.instructions:
    #         instr.accept2(self)

    @when(AST.Condition)
    def visit(self, node):
        if node.condition.accept2(self):
            node.instruction.accept2(self)
        elif node.else_instruction:
            node.else_instruction.accept2(self)

    # simplistic while loop interpretation
    @when(AST.WhileInstr)
    def visit(self, node):
        while node.condition.accept2(self):
            try:
                node.instruction.accept2(self)
            except BreakException:
                break
            except ContinueException:
                continue
       
    @classmethod
    def calculate(cls, op, r1, r2):
        return eval(str(r1) + str(op) + str(r2))

    @classmethod
    def current_scope(cls):
        if Interpreter.functionMemory.stack:
            return Interpreter.functionMemory
        else:
            return Interpreter.globalMemory

    @classmethod
    def evalNode(cls, self, node):
        value = None
        if isinstance(node, AST.Expression):
            return node.accept2(self)
        elif isinstance(node, AST.List):
            return node.accept2(self)
        elif (type(node.value) == str):
            value = Interpreter.current_scope().get(node.value)
            if value == None:
                value = Interpreter.globalMemory.get(node.value)
        elif node:
            value = node.accept2(self)
        return value

