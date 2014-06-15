
# import AST


# def addToClass(cls):

#     def decorator(func):
#         setattr(cls,func.__name__,func)
#         return func
#     return decorator

# def printTab(depth, value):
#     s = ""
#     for i in range(depth):
#         s += "| "
#     print s+str(value)


# class TreePrinter:

#     @addToClass(AST.Expression)
#     def printTree(self,depth):
#         pass


#     @addToClass(AST.Node)
#     def printTree(self,depth):
#         raise Exception("printTree not defined in class " + self.__class__.__name__)


#     @addToClass(AST.Const)
#     def printTree(self,depth):
#         printTab(depth,self.value)


#     @addToClass(AST.Declaration)
#     def printTree(self,depth):
#         printTab(depth,'=')
#         printTab(depth+1,self.left)
#         if type(self.right) == str:
#             printTab(depth+1,self.right)
#         else:
#             self.right.printTree(depth+1)


#     @addToClass(AST.Assignment)
#     def printTree(self,depth):
#         printTab(depth,'=')
#         printTab(depth+1,self.left)
#         if type(self.right) == str:
#             printTab(depth+1,self.right)
#         else:
#             self.right.printTree(depth+1)


#     @addToClass(AST.DeclarationList)
#     def printTree(self,depth):
#         if self.declarations != []:
#             printTab(depth,"DECL")
#             for decl in self.declarations:
#                 decl.printTree(depth+1)


#     @addToClass(AST.Function)
#     def printTree(self,depth):
#         printTab(depth,"FUNDEF")
#         printTab(depth+1,self.fun_name)
#         printTab(depth+1,"RET "+self.return_type)

#         if self.args_list != None:
#             for arg in self.args_list:
#                 arg.printTree(depth+1)

#         self.instr_list.printTree(depth)


#     @addToClass(AST.Arg)
#     def printTree(self,depth):
#         printTab(depth,"ARG "+self.name)


#     # @addToClass(AST.CompoundInstruction)
#     # def printTree(self,depth):
#     #     self.declarations.printTree(depth+1)
#     #     if self.instructions != None:
#     #         for instr in self.instructions:
#     #             instr.printTree(depth+1)


#     @addToClass(AST.Condition)
#     def printTree(self,depth):
#         printTab(depth,"IF")
#         self.condition.printTree(depth+1)
#         self.instruction.printTree(depth)
#         if self.else_instruction != None:
#             printTab(depth,"ELSE")   
#             self.else_instruction.printTree(depth)


#     @addToClass(AST.WhileInstr)
#     def printTree(self,depth):
#         printTab(depth,"WHILE")
#         self.condition.printTree(depth+1)
#         self.instruction.printTree(depth)


#     @addToClass(AST.FunCall)
#     def printTree(self,depth):
#         printTab(depth,"FUNCALL")
#         printTab(depth+1,self.fun_name)
#         for expr in self.expr_list:
#             if type(expr) == str:
#                 printTab(depth+1,expr)
#             else:
#                 expr.printTree(depth+1)




    
