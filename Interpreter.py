import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *

class Interpreter(object):

    globalMemory = MemoryStack(Memory("global"))
    functionMemory = MemoryStack(Memory("function"))
    functions = []


    @on('node')
    def visit(self, node):
        pass

    @when(AST.Program)
    def visit(self, node):
        node.declarations.accept2(self)
        for fundef in node.fundefs:
            fundef.accept2(self)
        for instr in node.instructions:
            instr.accept2(self)

    @when(AST.Const)
    def visit(self, node):
        return node.value

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = Interpreter.evalNode(self, node.left)
        r2 = Interpreter.evalNode(self, node.right)

        return Interpreter.calculate(node.operator, r1, r2)

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

    @when(AST.OneArgInstruction)
    def visit(self, node):
        value = Interpreter.evalNode(self, node.arg)

        if node.name == "PRINT":
            print value
        elif node.name == "RETURN":
            raise ReturnValueException(value)
        elif node.name == "BREAK":
            raise BreakException()
        else:
            raise ContinueException()

    @when(AST.CompoundInstruction)
    def visit(self, node):
        Interpreter.current_scope().push(Memory("compound_instruction"))
        node.declarations.accept2(self)
        for instr in node.instructions:
            instr.accept2(self)

    @when(AST.LabeledInstruction)
    def visit(self, node):
        node.instruction.accept2(self)

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
    
    @when(AST.RepeatUntilInstr)
    def visit(self, node):
        try:
            for instr in node.instructions:
                instr.accept2(self)
        except BreakException:
            return
        except Continue:
            pass

        while node.condition.accept2(self):
            try:
                for instr in node.instructions:
                    instr.accept2(self)
            except BreakException:
                break
            except ContinueException:
                continue    

    @when(AST.FunCall)
    def visit(self, node):
        for func in Interpreter.functions:
            if func.fun_name == node.fun_name:
                function = func
                break

        Interpreter.functionMemory.push(Memory(node.fun_name + "_scope"))
        for i in range(len(function.args_list)):
            value = Interpreter.evalNode(self,node.expr_list[i])
            Interpreter.functionMemory.insert(function.args_list[i].name, value)
        try:
            function.instr_list.accept2(self)
        except ReturnValueException as e:
            return e.value

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
        if type(node) == str:
            value = Interpreter.current_scope().get(node)
            if value == None:
                value = Interpreter.globalMemory.get(node)
        elif node:
            value = node.accept2(self)
        return value

