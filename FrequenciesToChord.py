from NoteFinder import *
from ChordIdentifier import *

def main():
	detected_frequencies = [261, 331, 392]
	identifier = ChordIdentifier()
	print(identifier.identify_chord(list(map(lambda x: note_finder(x)[1], detected_frequencies))));

if __name__ == '__main__':
	main()