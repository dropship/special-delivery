import os
import string
from distutils.version import LooseVersion

instruments = ['bass', 'chords', 'drums', 'voices']

for instrument in instruments:
	textfile = str(instrument) + "-info.txt"
	instrPath = str(instrument) + "/"
	
	output_file = open(textfile, 'w')
	
	count = 0
	prevBPM = str('0')
	
	files = os.listdir(instrPath)
	files.sort(key=LooseVersion)
	
	for filename in files:
		# Count of files per BPM
		if filename.endswith('.mid'):
			name = list(filename.partition('_'))
			bpm = str(name[0])
			if prevBPM != bpm:
				if count > 0:
					print >>output_file, str(instrument) + "-count " \
							+ str(prevBPM) + " " + str(count) + ","
				count = 0
				prevBPM = bpm
			count += 1
	print >>output_file, str(instrument) + "-count " \
			+ str(prevBPM) + " " + str(count) + ","
				
	for filename in files:
		# Output files				
		if filename.endswith('.mid'):
			name = list(filename.partition('_'))
			bpm = str(name[0])
			if prevBPM != bpm:
				count = 0
				prevBPM = bpm
			index = str(count)
			print >>output_file, str(instrument) + " " + bpm + " " \
					+ index + " " + str(filename) + ","
			count += 1
				
	print "Created: " + str(textfile)
print "Done."