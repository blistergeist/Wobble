"""
Chord Identifier: 
Simple lookup for the name of a chord matching
an unordered list of input notes. Can identify
major, minor, and augmented chords with or without
sevenths from their constituent notes. I don't know
any more chord types.
I also copied this header from Morgan.
Author: Jacob See
Date Created: 4/3/16
Date edited: 4/3/16
Windows 10 64-bit
Python 3.5.1 64-bit (Anaconda 2.4.1)
To get Anaconda/Miniconda: http://continuum.io/downloads
"""

class Chord:

	notes = ['A', 'A#/Bb', 'B', 'C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab']

	def nth_step(self, note, steps):
		return self.notes[(self.notes.index(note) + steps) % len(self.notes)]

	def __init__(self, baseNote='C'):
		self.baseNote = baseNote
		self.majorNotes = [baseNote, self.nth_step(baseNote, 4), self.nth_step(baseNote, 7)]
		self.minorNotes = [baseNote, self.nth_step(baseNote, 3), self.nth_step(baseNote, 7)]
		self.seventhNote = self.nth_step(baseNote, 10)
		self.augmentedNotes = [baseNote, self.nth_step(baseNote, 4), self.nth_step(baseNote, 8)]
		self.suspendedNotes = [baseNote, self.nth_step(baseNote, 5), self.nth_step(baseNote, 7)]

	def generate_permutations(self):
		permutations = {
			"major": self.majorNotes,
			"minor": self.minorNotes,
			"major seventh": self.majorNotes + [self.seventhNote],
			"minor seventh": self.minorNotes + [self.seventhNote],
			"augmented": self.augmentedNotes,
			"augmented seventh": self.augmentedNotes + [self.seventhNote],
			"suspended": self.suspendedNotes,
			"suspended seventh": self.suspendedNotes + [self.seventhNote]
		}
		return permutations


	def check_match_notes(self, notes: list):
		permutations = self.generate_permutations()
		for chord_type in permutations:
			if set(notes) == set(permutations[chord_type]):
				return self.baseNote + " " + chord_type
		return "No match"

class ChordIdentifier:

	def __init__(self):
		self.chords = chords = list(map(lambda x: Chord(x), Chord.notes))

	def identify_chord(self, notes: list):
		for chord in self.chords:
			result = chord.check_match_notes(notes)
			if result != 'No match':
				return result
		return 'Could not identify chord'

def main():

	notes = [['F', 'G#/Ab', 'C'], ['D', 'F', 'A#/Bb', 'G#/Ab'], ['D#/Eb', 'A#/Bb', 'F#/Gb'], ['A', 'C#/Db', 'G', 'F'], ['A', 'B', 'C']]
	identifier = ChordIdentifier()
	for note_set in notes:
		print(', '.join(note_set) + " --- " + identifier.identify_chord(note_set))

if __name__ == '__main__':
	main()