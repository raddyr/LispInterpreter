# #!/usr/bin/python

# from AST import *
# from ttype import *



# class TypeChecker(object):

#     error_found = False
#     return_type = None

#     @classmethod
#     def error(cls,msg,lineno):
#         print str(lineno) + ": error: ",msg + "."
#         TypeChecker.error_found = True

#     @classmethod
#     def warning(cls,msg,lineno):
#         print str(lineno) + ": warning: ",msg + "."

#     def visit_Expression(self,node):
#         pass

#     def visit_DeclarationList(self,node):
#         for decl in node.declarations:
#             decl.accept(self)

#     def visit_Declaration(self,node):
#         type1 = node.type;
#         type2 = node.right.accept(self)
#         if type1 != type2:
#             if type1 == 'float' and type2 =='int':
#                 TypeChecker.warning("casting from int to float",node.lineno)
#             else:
#                 TypeChecker.error("type mismatch; expected '" + str(type1) + "', got '" + str(type2) + "'",node.lineno)
#                 return "None"
        
#         if node.symbol_table.get(node.left) != None:
#             if node.symbol_table.found_in_parent == True:
#                 TypeChecker.warning("variable '" + node.left + "' is overriden",node.lineno)
#                 node.symbol_table.put(node.left, VariableSymbol(node.left,node.type))
#             else:
#                 TypeChecker.error("variable '" + node.left + "' was already declared",node.lineno)
                      
#         else:
#             node.symbol_table.put(node.left, VariableSymbol(node.left,node.type))


#     def visit_Const(self,node):
#         if (type(node.value) == int):
#             return "int"
#         elif (type(node.value) == float):
#             return "float"
#         else:
#             return "string"


#     # def visit_CompoundInstruction(self,node):
#     #     for decl in node.declarations.declarations:
#     #         decl.accept(self)
#     #     for instr in node.instructions:
#     #         instr.accept(self)

#     def visit_Assignment(self,node):
#         type1 = node.symbol_table.get(node.left)
#         if type1 != None:
#             type1 = type1.type
#         type2 = node.right
#         if type(type2) == str:
#             type2 = node.symbol_table.get(node.right)
#             if type2 == None:
#                 TypeChecker.error("undeclared variable '" + node.right +"'",node.lineno)
#                 return None
#             else:
#                 type2 = type2.type
#         else:
#             type2 = type2.accept(self)
#         if type1 == None:
#             TypeChecker.error("undeclared variable '" + node.left +"'",node.lineno)
#         elif type1 != type2:
#             if type1 == 'float' and type2 =='int':
#                 TypeChecker.warning("casting from int to float",node.lineno)
#             else:
#                 TypeChecker.error("type mismatch; expected '" + str(type1) + "', got '" + str(type2) + "'",node.lineno)


#     def visit_Function(self, node):
#         node.symbol_table.parent.put(node.fun_name, FunctionSymbol(node.fun_name, node.return_type, [a.type for a in node.args_list] if node.args_list else None))
#         if node.args_list:
#             for arg in node.args_list:
#                 arg.accept(self)
#         node.instr_list.accept(self)
    

#     def visit_Fun_Arg(self, node):
#         if node.symbol_table.get(node.name) != None and node.symbol_table.found_in_parent == False:
#             TypeChecker.error("duplicate function arguments - '" + node.name + "' was already declared",node.lineno)
#         else:
#             node.symbol_table.put(node.name, VariableSymbol(node.name, node.type))
            
#     def visit_Condition(self,node):
#         node.condition.accept(self)
#         node.instruction.accept(self)
#         if node.else_instruction:
#             node.else_instruction.accept(self)
        
#     def visit_WhileInstr(self,node):
#         node.condition.accept(self)
#         node.instruction.accept(self)


#     def visit_FunCall(self,node):
#         fun = node.symbol_table.get(node.fun_name)
#         if fun == None:
#             TypeChecker.error("undeclared function '" + node.fun_name + "()'",node.lineno)
#             return None

#         if len(node.expr_list) != len(fun.args):
#             TypeChecker.error("invalid number of parameters; expected " + str(len(fun.args)) + ", got " + str(len(node.expr_list)),node.lineno)
#         else:
#             for i in range(len(fun.args)):
#                 type1 = node.expr_list[i]
#                 if type(type1) == str:
#                     if node.symbol_table.get(type1) == None:
#                         TypeChecker.error("undeclared variable '" + str(type) + "'" ,node.lineno)
#                         return None
#                     else:
#                         type1 = node.symbol_table.get(type1).type
#                 else:
#                     type1 = node.expr_list[i].accept(self)
#                 type2 = fun.args[i]
#                 if type1 != type2:
#                     if type1 == 'int' and type2 =='float':
#                         TypeChecker.warning("function call - casting from int to float",node.lineno)
#                     else:
#                         TypeChecker.error("invalid function argument type; expected '" + str(type2) + "', got '" + str(type1) + "'",node.lineno)
#                         return None

#         return fun.type
