import Interpreter

builtIns = {
	'+' : lambda x: reduce(lambda d,y: d+y, x),
	'-' : lambda x: reduce(lambda d,y: d-y, x),
	'*' : lambda x: reduce(lambda d,y: d*y, x),
	'/' : lambda x: reduce(lambda d,y: d/y, x),

	'car': lambda x: x[0][0],
	'cdr': lambda x: x[0][1:],
	'subseq': lambda x: x[2][x[0]:x[1]],
	'nth': lambda x: x[1][x[0]],

	'print' : lambda x: evalPrint(x[0]),
	'setq' : lambda x: evalSetq(x),
	# 'cond' : lambda x: evalCond(x)
}

def evalPrint(x):
	print x
	return x

def evalSetq(x):        
	# if Interpreter.current_scope().set(x[0], x[1]) == False: //NIE OBSLUGUJEMY BO SETQ GLOBALNE?
		if Interpreter.Interpreter.globalMemory.set(x[0], x[1]) == False:
			Interpreter.Interpreter.globalMemory.insert(x[0], x[1])
		return x[1]

def evalCond(x):
	for i in range(len(x)):
		if Interpreter.evalNode(x[i][0]):
			for j in range(len(x[i])-1):
				res = Interpreter.evalNode(x[i][j+1])
			return res
	return None

# print builtIns['subseq']((1, 2, 3, 4), 1, 3)
# try:
# 	print a['cdr'](1)
# except TypeError as e:
# 	print "Wrong argument to"
# 	print e

