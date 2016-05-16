'''
transpose.py
Transposes a piece from one key to another 
'''
from itertools import repeat
from helper import flatten

FLATS = ["_A","A","_B","B","C","_D","D","_E","E","F","_G","G"]
SHARPS = ["^G","A","^A","B","C","^C","D","^D","E","F","^F","G"]
ENHARMONICS = {"^B": "C", "_C":"B", "^E":"F","_F":"E"} # enharmonics that should be changed

NOTES = set(FLATS) | set(SHARPS)

# Transposes note from key1 to key2. 
def transpose(note, key1, key2):
	# finds accidental type of key. Prefers sharps.
	def sharp_or_flat(key_or_note): 
		return SHARPS if key_or_note in SHARPS else FLATS
	# finds distance between two keys/notes
	def distance(acc1, acc2):
		return acc2.index(key2) - acc1.index(key1)
	# changes "weird" note name to enharmonic note.
	lowercase = note.islower()
	note = note.upper()
	if note in ENHARMONICS:
		note = ENHARMONICS[note]
	
	acc_type1 = sharp_or_flat(key1) # "accidental" type of key1
	acc_type2 = sharp_or_flat(key2) 
	note_type = sharp_or_flat(note)
	
	spillover = flatten(repeat(acc_type2, 2))
	skew = distance(acc_type1, acc_type2)
	transposed = spillover[note_type.index(note) + skew]
	if lowercase:
		transposed = transposed.lower()
	return transposed

def transpose_line(line, key1, key2):
	note = ""
	transposed = ""
	for i in range(len(line)):
		if line[i] in "^_": # these are accidentals, 
			note += line[i] # so they're considered part of the next note
							# for now we ignore '=' (natural)
		elif line[i].upper() in NOTES: 
			transposed += transpose(note + line[i], key1, key2)
			note = ""
		else: # otherwise, we have something irrelevant to pitch. We ignore it.
			transposed += line[i]
	return transposed

def transpose_piece(piece, key2):
	data = piece[0] 
	key1 = piece[1]["K"]
	return [transpose_line(line, key1, key2) for line in data]