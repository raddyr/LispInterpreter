builtIns = {
	'+' : lambda x: x[0]+x[1],
	'-' : lambda x: x-y,
	'*' : lambda x: x*y,
	'/' : lambda x: x/y,

	'car': lambda x: x[0],
	'cdr': lambda x: x[1:],

	'1+': lambda x: x +1,
	'1-': lambda x: x -1,

	'subseq': lambda x, a, b: x[a:b],
	'nth': lambda nth, x: x[nth],

}


# print builtIns['subseq']((1, 2, 3, 4), 1, 3)
# try:
# 	print a['cdr'](1)
# except TypeError as e:
# 	print "Wrong argument to"
# 	print e

