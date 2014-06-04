import fileinput
import sys

Ionian = [ "maj", "maj6/9", "maj7", "maj9", "majadd9" ]
IonianSus = [ "sus" ]
Dorian = [ "min", "min6/9", "min9", "min7", "min11" ]
Aeolian	= [ "minb6", "min7b6" ]
AeolianDom	= [ "7b6" ]
Locrian	= [ "min7b5b9" ]
Lydian = [ "maj7#11", "maj#11" ]
LydianDom = [ "7#11", "13#11" ]
Mixolydian = [ "dom7", "7sus", "13sus", "dom13" ]
DomSus = [ "7sus4" ]
HalfDim	= [ "m7b5", "min7b5" ]
Diminished = [ "7b913" , "7b9"]
Diminished2 = [ "dim7" ]
Altered = [ "7alt", "7b9" ]
MelodicMin	= [ "minmaj7" ]
HarmonicMin	= [ "minb6#7" ]
WholeTone = [ "7aug" ]
Phrygian = [ "minb2" ]
PhrygianDom	= [ "7b9b13" ]

chordDict = { 'I': 0, 'bII': 1, 'II': 2, '#II': 3, 'bIII': 3,
			  'III': 4, 'IV': 5, '#IV': 6, 'bV': 6, 'V': -5, '#V': -4,
			  'bVI': -4, 'VI': -3, '#VI': -2, 'bVII': -2, 'VII': -1 }
			
# chordDict = { 'I': 0, 'bII': 1, 'II': 2, '#II': 3, 'bIII': 3,
# 	  'III': 4, 'IV': 5, '#IV': 6, 'bV': 6, 'V': 7, '#V': 8,
# 	  'bVI': 8, 'VI': 9, '#VI': 10, 'bVII': 10, 'VII': 11 }
			
modeList = [ Ionian, IonianSus, Dorian, Aeolian, AeolianDom, Locrian, Lydian,
			LydianDom, Mixolydian, DomSus, HalfDim, Diminished, Diminished2,
			Altered, MelodicMin, HarmonicMin, WholeTone, Phrygian, PhrygianDom ]

slashExtDict = { '-': -1, '/I': 0, '/bII': 1, '/II': 2, '/bIII': 3,
				'/III': 4, '/bIV': 4, '/IV': 5, '/bV': 6, '/V': 7, '/bVI': 8,
				'/VI': 9, '/bVII': 10, '/VII': 11, 'slashI': 0, 'slashbII': 1,
				'slashII': 2, 'slashbIII': 3, 'slashIII': 4, 'slashIV': 5,
				'slashbV': 6, 'slashV': 7, 'slashbVI': 8, 'slashVI': 9,
				'slashbVII': 10, 'slashVII': 11 }

def isModeValid(inputMode):
	doesModeExist = False
	for mode in modeList:
		if inputMode in mode:
			doesModeExist = True
			break
	return doesModeExist

def firstModeInModeList(inputMode):
	firstMode = "INVALID"
	for mode in modeList:
		if inputMode in mode:
			firstMode = mode[0]
			break
	return firstMode
	
def validateLine(lineNum, line):
	error = 1
	if len(line) != 12:
		print"Error (Line " + str(lineNum) + "): line does not contain 12 items."
		error = 0
	for value in range(len(line)):
		if (value % 3 == 0): # Chord symbol
			if not (line[value] in chordDict):
				print"Error (Line " + str(lineNum) + "): " \
						+ str(line[value]) + " is invalid."
				error = 0
		elif (value % 3 == 1): # Scale Mode
			doesModeExist = False
			if not isModeValid(line[value]): 
				print"Error (Line " + str(lineNum) + "): " \
						+ "mode '" + str(line[value]) + "' is invalid."
				error = 0
		if (value % 3 == 2): # Slash Extension
			if not line[value] in slashExtDict:
				print"Error (Line " + str(lineNum) + "): " \
						+ str(line[value]) + " is invalid."
				error = 0
	return error


def printChordList():
	for chord in range(len(chordList)):
		print str(chord) + ": " + str(chordList[chord])

def printInputFile(index):
	print "Input File:"
	for line in fileinput.input(sys.argv[index]):
		rawProgression = line.split()
		newProgression = []
		chord = []
		for value in range(len(rawProgression)):
			chord.append(rawProgression[value])
			# Chord lists are in the format [Chord, mode, slashExt]
			if ((value % 3) == 2):
				newProgression.append(chord)
				chord = []
				continue
		print newProgression

def printOutputFile(index):
	print "Output File:"
	for line in fileinput.input(sys.argv[index]):
		inputLine = line.split()
		lineNum = fileinput.filelineno()
		newProgression = []
		newChord = []
		error = 0
		if not validateLine(lineNum, inputLine):
			error = 1
		for value in range(len(inputLine)):
			inputValue = inputLine[value]
			if (value % 3 == 0): # Chord Symbol
				newChord.append(chordDict[inputLine[value]])
			elif (value % 3 == 1): # Scale Mode			
				newChord.append(firstModeInModeList(inputLine[value]))
			elif ((value % 3) == 2): # Slash Extension
				newChord.append(slashExtDict[inputLine[value]])
				newProgression.append(newChord)
				newChord = []
		print lineNum, newProgression
		if error == 1:
			print
		
def validateChordProgFile(filename, fileIndex):
	outputFile = open(str(filename) + '.txt', 'w')
	for line in fileinput.input(sys.argv[fileIndex]):
		inputLine = line.split()
		inputLineNum = fileinput.filelineno()
		if not validateLine(inputLineNum, inputLine):
			print "Input file has errors, process aborted."
			break
		outputFile.write("%d " % inputLineNum)
		for value in range(len(inputLine)):
			inputValue = inputLine[value]
			if (value % 3 == 0): # Chord Symbol
				outputFile.write("%s " % chordDict[inputValue])
			elif (value % 3 == 1): # Scale Mode			
				outputFile.write("%s " % firstModeInModeList(inputValue))
			elif ((value % 3) == 2): # Slash Extension
				outputFile.write("%s " % slashExtDict[inputValue])
			if (value == len(inputLine) - 1):
				outputFile.write(",\n")
	outputFile.close()

def main():
	
	if (len(sys.argv) == 3) and (str(sys.argv[1]) == "-p"):
		# Print output to terminal window
		fileName = sys.argv[2].partition('.')[0]
		fileIndex = 2
		print " --- Converting " + str(fileName) + ".tsv to " + str(fileName) + ".txt ---"
		print printInputFile(fileIndex)
		print
		print printOutputFile(fileIndex) 
		print
	else: 
		fileName = sys.argv[1].partition('.')[0]
		fileIndex = 1
		print " --- Converting " + str(fileName) + ".tsv to " + str(fileName) + ".txt ---"

	validateChordProgFile(fileName, fileIndex)
	print "Done."

if __name__ == "__main__":
    main()
