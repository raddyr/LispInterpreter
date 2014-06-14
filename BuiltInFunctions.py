import Interpreter

builtIns = {
	'+' : lambda x: reduce(lambda d,y: d+y, x),
	'-' : lambda x: reduce(lambda d,y: d-y, x),
	'*' : lambda x: reduce(lambda d,y: d*y, x),
	'/' : lambda x: reduce(lambda d,y: d/y, x),

	'car': lambda x: x[0][0],
	'cdr': lambda x: x[0][1:],

	'1+': lambda x: x[0] +1,
	'1-': lambda x: x[0] -1,

	'subseq': lambda x, a, b: x[0][a:b],
	'nth': lambda nth, x: x[0][nth],

	'print' : lambda x: my_print(x[0]),

	'setq' : lambda x: Interpreter.Interpreter.globalMemory.insert(x[0], x[1]),
	'cond' : lambda x: evalCond(x)
}

def my_print(x):
	print x
	return x

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

