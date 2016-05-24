# Noodle

## Author
Daniel J. Rothblatt, February 2016

## Description
This program generates a Markov model of a corpus of music transcribed
in ABC notation. ABC notation is a simple, easily readable music
transcription system used largely to transcribe folk music. As a
result, the data provided in big_guy.abc is a corpus of English folk
music.

## The Files
- README.md: This file
- big_guy.abc: Music collection in ABC notation
- clean_keys.sed: Preprocesses keys to a uniform format
- clear_comments.sed: Removes comments from ABC files
- fix_meters.sed: Changes meter to a known meter if unknown meter
- helper.py: Auxiliary functions that prove useful in other libraries
- prepare.py: Separates data from metadata in each piece and prepares
pieces for noodle.py
- rhythm.py: Computes duration of a musical phrase
- transpose.py: Transposes a piece to a target key
- noodle.py: Generates a piece of music from input by building a
Markov model.
- music_generator.py: *RUN THIS!* Reads in a user-specified ABC file
and outputs a piece of music.

## Purpose
This project was inspired by David Pesetsky and Jonah Katz of
MIT. Their Identity Thesis for Music claims that music and language
have fundamentally the same syntactic structure--the only difference
being the types of elements that are treated as syntactic objects.
A prediction that the Identity Thesis puts forward is that a Markov
model is wholly inadequate for producing music: Just as a Markov model
of the syntax of a language will always be able to generate
ungrammatical sentences (because syntax is not a regular language), a
Markov model of the structure of music _should_ generate
"ungrammatical" music. The question was, "What would ungrammatical
music look like?"
The tentative conclusion of this project is that "ungrammatical" music
is atonal--pieces may modulate freely from key to key without ever
returning to the tonic (initial key of a piece), because the linear
nature of a Markov model prevents it from remembering what the tonic
is. However, the project as it currently stands has major flaws that
make this conclusion only a tentative one. (See "To Do" below.)

## Use
Run music_generator.py from the command line.

### Grammar
    <command> ::= python3 music_generator.py <unary_flag>*
    <unary_flag> ::= <file_flag> | <meter_flag> | <length_flag> |
    <key_flag>
    <file_flag> ::= (-i | --in | -o | --out) \w+.abc

### Semantics
    Unary Flags
          - file: indicates input or output file
          - meter: specifies the meter of the piece (what type of note
          gets the beat, how many beats per measure). Note that the
          note that gets the beat should always be a power of 2
          greater than or equal to 1 (i.e., for all m,n: m/2^n)
          - length: specifies how many beats per measure. Should be an
          integer.
          - key: specifies the key of the piece.

## To Do
   I (Daniel Rothblatt) do not consider this project complete in the
   slightest. The major problems currently facing Noodle are listed
   here, as well as in music_generator.py:
  - This project does not really generate bar lines (measure
  delimiters) in a sensible way yet. The author was under the
  assumption that the bar lines would be easier to insert than they
  in fact are.
  - This project does not handle anything but note duration and
  pitch--additional work would enable it to keep track of things like
  dynamics and ties.

