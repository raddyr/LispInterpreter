
class Symbol(object):

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Memory:

    def __init__(self, name): # memory name
        self.name = name
        self.data = []  #list of Symbol

    def has_key(self, name):  # variable name
        for element in self.data:
            if element.name == name:
                return True
        return False

    def get(self, name):         # get from memory current value of variable <name>
        for element in self.data:
            if element.name == name:
                return element.value
        return None

    def insert(self, name, value):  # puts into memory current value of variable <name>
        self.data.append(Symbol(name, value))

    def set(self, name, value):  # sets value of variable <name>
        for element in self.data:
            if element.name == name:
                element.value = value
                return True
        return False

class MemoryStack:
                                                                             
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        if memory != None:
            self.stack = [memory]   #list of Memory
        else:
            self.stack = []

    def get(self, name):             # get from memory stack current value of variable <name>
        for i in range(len(self.stack)):
            val = self.stack[-i-1].get(name)
            if val != None:
                return val
        return None

    def insert(self, name, value): # puts into memory stack current value of variable <name>
        self.stack[len(self.stack)-1].insert(name, value)

    def set(self, name, value): # sets value of variable <name>
        for i in range(len(self.stack)):
            val = self.stack[-i-1].get(name)
            if val != None:
                return self.stack[-i-1].set(name, value)
        return False

    def push(self, memory): # push memory <memory> onto the stack
        self.stack.append(memory)

    def pop(self):          # pops the top memory from the stack
        if self.stack == []:
            return None
        else:
            return self.stack.pop()

