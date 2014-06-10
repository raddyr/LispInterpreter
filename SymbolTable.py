#!/usr/bin/python


class VariableSymbol(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type


class FunctionSymbol(object):

    def __init__(self, name, type, args):
        self.name = name
        self.type = type    # function return type
        self.args = args


class SymbolTable(object):

    def __init__(self, parent, name):
        self.table = {}
        self.parent = parent
        self.name = name
        self.found_in_parent = False

    def put(self, name, symbol):
        self.table[name] = symbol

    def get(self, name):
        n = self.table.get(name)
        if (n == None) and self.parent:
            self.found_in_parent = True
            return self.parent.get(name)
        self.found_in_parent = False
        return n

    def getParentScope(self):
        return self.parent





