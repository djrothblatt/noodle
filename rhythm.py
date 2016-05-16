'''
rhythm.py

This module handles issues of rhythm in ABC.

OVERVIEW: Every piece has a meter (M)
'''

NOTES = "ABCDEFGabcdefg" # these are rhythms--we don't care about accidentals here

# gets the duration of a phrase. "beat" was a very bad choice of term. CHANGE
def duration(beat):
	stop = len(beat)
	i = 0
	curr_len, total_len = 0, 0 # curr_len is length of current note, total_len length of phrase
	factor = "" # scaling factor for shorter and longer notes, as string
	while i < stop:
		if beat[i] in NOTES:
			total_len += curr_len
			curr_len = 1
		while beat[i] in "123456789": # note lasts k times longer for k in this list
			factor += beat[i]
			i += 1
		if factor:
			curr_len *= int(factor)
			factor = ""
		if beat[i] == "/": # note lasts k times shorter for following number k
			i += 1
			# print("beat[i]:", beat[i])
			factor = ""
			while beat[i] in "123456789":
				factor += beat[i]
				i += 1
			if factor: 
				curr_len /= int(factor)
				factor = ""
		i += 1
	total_len += curr_len
	return round(total_len, 3)