'''
music_generator.py
by Daniel J. Rothblatt

This project attempts to generate music by creating a Markov model
of a textual representation of a piece/collection of pieces.

The motivation for this project is to understand a prediction
made by Pesetsky & Katz's Identity Thesis for Music:
Since P&K claim that music and language use the same syntax, it 
follows that a Markov model of music will be in some way inadequate,
as Markov models are inadequate for linguistic syntax. 

This project will use ABC notation to represent music.
This project's test corpus will be from the Village Music Project
(village-music-project.org.uk), a collection of collections of
English folk music.

CURRENT PROBLEMS:
	* Handling repeats:
		You are currently treating repeats as part of the phrase that follows
		Easy fix for now: just ignore repeats -- DONE
		TO DO: Implement repeats
	* Working within the meter:
		You need to keep track of how many beats have been used
		Good idea to put it in another module
		SOLUTION: Add bar lines after generation
			Problem: Need to write in ties when you go over the beats/measure... 
		ALTERNATIVE: Need to compare how many beats a phrase takes up to how many
			beats are left in the measure and reroll if you don't have enough space.
		The second choice is somewhat ad-hoc, but good enough for what we want.
		For now we implement the second solution.
		TO DO: Implement first solution in another program.
SOLVED PROBLEMS:
	* Issues with data:
		Transcribers left comments below key declaration.
		SOLUTION: The comments are uniformly delimited by "..."! 
		Just ignore/remove text between ""!
		PROBLEM SOLVED -- wrote clear_comments.sed to preprocess data
'''

from sys import argv
import transpose
import prepare
import noodle

INFILE = "wm_clarke.abc"
OUTFILE = "out.abc"
METER = "6/8" # we would like meters to match up
BEATS_PER_MEASURE = int(METER[:METER.find("/")]) # beats in a measure
KEY = "C" # we would like everything to be in the same key;
# 			it's the intervals that are important, not the absolute pitches.

for i in range(len(argv)):
	arg = argv[i]
	if arg in ["-i", "--in"]:
		INFILE = argv[i+1]
	if arg in ["-o", "--out"]:
		OUTFILE = argv[i+1]
	if arg == ["-m", "--meter"]:
		METER = argv[i+1]
	if arg == ["-l", "-L", "--mlength"]:
		BEATS_PER_MEASURE = argv[i+1]
	if arg == ["-k", "--key"]:
		KEY = argv[i+1]

my_file = open(INFILE, "r")
lines = my_file.readlines()
my_file.close()

# convert lines of our file into a list of pieces
pieces = prepare.prepare(lines)
pieces = [piece for piece in pieces if piece[0][0] != "###"]

to_delete = []
for i in range(len(pieces)):
	try:
		pieces[i][1]["M"]
	except KeyError:
		# print("piece has no meter:", piece)
		# print("piece without meter:",piece[0])
		# piece[1]["M"] = "6/8"
		to_delete.append(i)
		# del pieces[i]
for i in range(len(pieces)):
	try:
		pieces[i][1]["K"]
	except KeyError:
		# print("piece without key:",piece[0])
		# piece[1]["K"] = "C"	
		# del pieces[i]
		to_delete.append(i)
pieces = [pieces[i] for i in range(len(pieces)) if i not in to_delete]

# PREPROCESSING:
# We filter out the correct meter and then transpose everything to one key.
correct_meter = [piece for piece in pieces if piece[1]["M"] == METER]  
transposed_pieces = [transpose.transpose_piece(piece, KEY) for piece in correct_meter]
transposed_data = [" ".join(tp) for tp in transposed_pieces]

# Building the Markov noodler
chain = noodle.build_chain(transposed_data)
out = noodle.gen_piece(chain, BEATS_PER_MEASURE)
f = open(OUTFILE, "a")
print(out, file=f)
print("\n", file=f)
f.close()