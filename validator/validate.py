#! /usr/bin/env python3

# Voices cannot cross
# No parallel octaves
# No parallel fifths
# 7th downward by step
# All notes required of harmony are present

import sys

if len(sys.argv) < 2:
    print('Must provide an input file')
    exit()

input = sys.argv[1]

# 0 = soprano
# 1 = alto
# 2 = tenor
# 3 = bass
voices = [[], [], [], []]
harmony = []

with open(input) as input_data:
    line_index = 0

    for line in input_data:
        stripped = line.rstrip()

        for i in range(0, len(stripped), 2):
            element = stripped[i:i+2]

            if line_index < 4:
                voices[line_index].append(int(element))
            else:
                harmony.append([element[0], element[1]])

        line_index += 1

# Calculate intervals between voices
# 0 = between soprano and alto (0, 1)
# 1 = between soprano and tenor (0, 2)
# 2 = between soprano and bass (0, 3)
# 3 = between alto and tenor (1, 2)
# 4 = between alto and bass (1, 3)
# 5 = between tenor and bass (2, 3)
intervals = [[], [], [], [], [], []]

for i in range(1, len(voices[0])):
    intervals[0].append((voices[0][i] - voices[1][i]) % 12)
    intervals[1].append((voices[0][i] - voices[2][i]) % 12)
    intervals[2].append((voices[0][i] - voices[3][i]) % 12)
    intervals[3].append((voices[1][i] - voices[2][i]) % 12)
    intervals[4].append((voices[1][i] - voices[3][i]) % 12)
    intervals[5].append((voices[2][i] - voices[3][i]) % 12)

for i in range(0, len(intervals)):
    for j in range(0, len(intervals[i])):
        consecutive_intervals = intervals[i][j:j+2]

        if consecutive_intervals == [0, 0] or consecutive_intervals == [7, 7]:
            print('parallel at ' + str(i) + ' ' + str(j))
