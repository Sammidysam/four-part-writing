#! /usr/bin/env python3
# A little utility for converting pitches in our decimal form into scientific pitch notation (e.g. 33 -> A4)
# Should be given an argument which is an uninterrupted line of pitches (e.g. 33333434333129)
# Or, optional flag -f followed by filename to instead give it a .4pw file as input instead

import sys

pitches = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'G#', 'A', 'Bb', 'B']

if len(sys.argv) < 2:
    print('Must provide an input')
    exit()

elif sys.argv[1] == '-f':
    with open(sys.argv[2]) as input_data:
        line_index = 0

        for line in input_data:
            notes = []
            if line_index == 4:
                exit()

            stripped = line.rstrip()
            for i in range(0, len(stripped), 2):
                partial = stripped[i:i+2]
                if partial == '??':
                    notes.append('??')
                else:
                    octave, pitch = divmod(int(partial), 12)
                    notes.append(pitches[pitch] + str(octave + 2))
            print(' '.join(notes))

            line_index += 1

else:
    line = []
    for i in range(0, len(sys.argv[1]), 2):
        octave, pitch = divmod(int(sys.argv[1][i:i+2]), 12)
        line.append(pitches[pitch] + str(octave + 2))
    print(' '.join(line))
