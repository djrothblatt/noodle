'''
helper.py

A collection of helper functions that are useful in multiple files.
'''
# Quickly flattens a 2D list. To be used with repeat.
def flatten(L):
	return [x for sublist in L for x in sublist]

# Creates a pair of lists: ({x|pred(x)}, {x|~pred(x)})
def list_split(pred, L):
	return ([x for x in L if pred(L)], [x for x in L if not pred(L)])