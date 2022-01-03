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
VOICE_COMBINATIONS = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
intervals = [[], [], [], [], [], []]

# Todo fix naming so that this all makes more sense?
# Returns None if either voice has no motion.
# Otherwise, returns the interval between the two voices at voice_index.
def interval_between_voices(voice_combination, voice_index):
    return (None
        if
            voices[voice_combination[0]][voice_index] == voices[voice_combination[0]][voice_index - 1] or
            voices[voice_combination[1]][voice_index] == voices[voice_combination[1]][voice_index - 1]
        else
            (voices[voice_combination[0]][voice_index] - voices[voice_combination[1]][voice_index]) % 12
    )

for voice_index in range(1, len(voices[0])):
    for index, combination in enumerate(VOICE_COMBINATIONS):
        intervals[index].append(interval_between_voices(combination, voice_index))

for i in range(0, len(intervals)):
    for j in range(0, len(intervals[i])):
        consecutive_intervals = intervals[i][j:j+2]

        if consecutive_intervals == [0, 0] or consecutive_intervals == [7, 7]:
            print('parallel at ' + str(i) + ' ' + str(j))
