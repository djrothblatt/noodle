'''
noodle.py

Markov "noodler" for music--because "babbling" isn't a musical sort of name.

The noodler will build a model one line of music at a time.
'''

from sys import argv
from random import random, choice
from rhythm import duration
THRESHOLD = 0.025

def build_chain(data):
	chain = {}
	for piece in data:
		measures = piece.split("|")
		beats = " ".join(measures)
		beats = beats.split(" ")
		for i in range(len(beats)):
			try:
				first, second, third = 	(beats[i], duration(beats[i])), \
										(beats[i+1], duration(beats[i+1])), \
										(beats[i+2], duration(beats[i+2]))
			except IndexError:
				break
			# if i == 0: # if we want to make special designated phrases to begin a piece...
			# 	first = '#' + first # but we really don't.
			key = (first, second)
			if key in chain:
				chain[key].append(third)
			else:
				chain[key] = [third]
	return chain

# This function needs to be altered to keep track of meter
# This change will probably allow us to remove the "###" end marker
# YOU SHOULD CHANGE THIS: Each measure is currently treated as its own domain.
def gen_phrase(chain, measure_length):
	key = choice([key for key in chain.keys()])
	beats = [] 
	first, second = key
	beats.append(first[0][1:])
	beats.append(second[0])
	curr_len = first[1] + second[1]
	fails = 0 # number of times we fail to fit a phrase into the measure
	go = 1.0
	while go > THRESHOLD:
		while curr_len < measure_length:
			try:
				third = choice(chain[key])
			except KeyError:
				break
			# print("chain[\"###\"]:", chain["###"])
			# if third == "###":
			# 	print("third:",third)
			# 	return '|'.join(beats)
			if curr_len + third[1] <= measure_length:
				beats.append(third[0])
				curr_len += third[1]
				key = (second, third)
				first, second = key	
			else:
				fails += 1
				if fails >= 10: # I'll give you ten chances...
					fails = 0
					break
		if beats[-1] != "|":
			beats.append("|")
		go = random()
	return ' '.join(beats)

def gen_piece(chain, measure_length):
	piece = ""
	go = 1.0
	while go > THRESHOLD:
		piece = piece + gen_phrase(chain, measure_length)
		go = random()
		# print("...")
	return piece