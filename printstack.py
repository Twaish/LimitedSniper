stack = []
def add(t):
	global stack
	stack.append(t)
def empty():
	global stack
	for t in stack:
		print(t)
	stack = []