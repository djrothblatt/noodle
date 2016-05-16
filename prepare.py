'''
prepare.py

Breaks text up into individual pieces and separates data from metadata in each piece.
This module prepares pieces for analysis by the Markov noodler.
'''
from helper import flatten, list_split
import re

METATAGS = [char + ":" for char in "AKLMNOQRSTWXZ"]
# X: index (in a collection of pieces)
# T: title
# M: meter
# R: genre
# 

# get_pieces: [string] -> [[string]]
# turns uncategorized lines into a list of pieces, where a piece is a list of lines.
# (A line is represented as a string.)
def get_pieces(lines):
	pieces = []
	piece = []
	data = [line for line in lines if line[0] != "%"] # '%' indicates comments in ABC
	for line in data:
		if line[0] == "\n":
			piece.append("###") # end of piece implicit in ABC. Let's make it explicit.
			pieces.append(piece)
			piece = [] # we've reached the end of the piece
		else:
			stripped = re.sub("[!\n]", "", line)
			# stripped = line[:-1] if line[-1] == "\n" else line
			# if stripped[-1] == "!": #'!' indicates a line break--unnecessary here
			# 	stripped = stripped[:-1]
			piece.append(stripped)
	return pieces

# This enables us to look up the key, meter, genre, &c., of our piece.
def metadata_dict(metadata):
	return {m[0]:m[2:] for m in metadata}

# splits a piece into data and metadata
def get_data_and_metadata(piece):	
	metadata = [piece[i] for i in range(len(piece)) if piece[i][:2] in METATAGS]
	data = [piece[i] for i in range(len(piece)) if piece[i] not in metadata]
	data = [re.sub(":","", d) for d in data] # removes repeats from data
	return (data, metadata_dict(metadata))

# turns lines of input into pieces separated into (data, metadata)
def prepare(lines):
	pieces = get_pieces(lines)
	return [get_data_and_metadata(piece) for piece in pieces]