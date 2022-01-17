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

# Extra configuration of the validator can go in later arguments.
rest_of_args = sys.argv[2:]

if '-o5' in rest_of_args:
    omit_fifth = True
else:
    omit_fifth = False

# 0 = soprano
# 1 = alto
# 2 = tenor
# 3 = bass
VOICE_NAMES = ['soprano', 'alto', 'tenor', 'bass']
voices = [[], [], [], []]
harmony = []

with open(input) as input_data:
    line_index = 0

    for line in input_data:
        stripped = line.rstrip()

        reading_harmony = line_index >= 4
        chars_to_read = 3 if reading_harmony else 2

        for i in range(0, len(stripped), chars_to_read):
            element = stripped[i:i+chars_to_read]

            if reading_harmony:
                harmony.append([element[0], element[1], element[2]])
            else:
                voices[line_index].append(int(element))

        line_index += 1

# Confirm all voices are in proper ranges.
ranges = [[24, 45], [19, 38], [12, 33], [0, 24]]

for voice_index, voice in enumerate(voices):
    for note_index, note in enumerate(voice):
        if note < ranges[voice_index][0] or note > ranges[voice_index][1]:
            print(VOICE_NAMES[voice_index] + ' out of range at beat ' + str(note_index + 1))

# Calculate intervals between voices
# 0 = between soprano and alto (0, 1)
# 1 = between soprano and tenor (0, 2)
# 2 = between soprano and bass (0, 3)
# 3 = between alto and tenor (1, 2)
# 4 = between alto and bass (1, 3)
# 5 = between tenor and bass (2, 3)
VOICE_COMBINATION_NAMES = ['soprano+alto', 'soprano+tenor', 'soprano+bass', 'alto+tenor', 'alto+bass', 'tenor+bass']
VOICE_COMBINATIONS = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
intervals = [[], [], [], [], [], []]

# Todo fix naming so that this all makes more sense?
# Returns None if either voice has no motion.
# Otherwise, returns the interval between the two voices at voice_index.
def interval_between_voices(voice_combination, note_index):
    return (None
        if
            voices[voice_combination[0]][note_index] == voices[voice_combination[0]][note_index - 1] or
            voices[voice_combination[1]][note_index] == voices[voice_combination[1]][note_index - 1]
        else
            (voices[voice_combination[0]][note_index] - voices[voice_combination[1]][note_index]) % 12
    )

for note_index in range(1, len(voices[0])):
    for index, combination in enumerate(VOICE_COMBINATIONS):
        intervals[index].append(interval_between_voices(combination, note_index))

for i in range(0, len(intervals)):
    for j in range(0, len(intervals[i])):
        consecutive_intervals = intervals[i][j:j+2]

        if consecutive_intervals == [0, 0] or consecutive_intervals == [7, 7]:
            fifth = consecutive_intervals == [7, 7]

            print('parallel ' + ('fifth' if fifth else 'octave') + ' between ' + VOICE_COMBINATION_NAMES[i] + ' at beat ' + str(j + 1) + ' into beat ' + str(j + 2))

# Voices cannot cross
for i in range(0, 3):
    top_voice = i
    bottom_voice = i + 1

    for note_index in range(0, len(voices[0])):
        if voices[top_voice][note_index] < voices[bottom_voice][note_index]:
            print('voice cross between ' + VOICE_NAMES[top_voice] + ' and ' + VOICE_NAMES[bottom_voice] + ' at beat ' + str(note_index + 1))

# All notes required of harmony are present.
def notes_for_harmony(chord):
    starting_note = int(chord[0], 16)
    decoration = chord[1]

    if decoration == 'M':
        intervals = [4] if omit_fifth else [4, 7]
    elif decoration == 'm':
        intervals = [3] if omit_fifth else [3, 7]
    elif decoration == '7':
        intervals = [4, 10] if omit_fifth else [4, 7, 10]
    elif decoration == 'd':
        intervals = [3, 10] if omit_fifth else [3, 6, 10]
    elif decoration == 'D':
        intervals = [3, 9] if omit_fifth else [3, 6, 9]
    elif decoration == 'b':
        intervals = [3] if omit_fifth else [3, 6]
    else:
        print('unknown chord decoration ' + decoration)

    notes = [starting_note]

    for interval in intervals:
        notes.append((starting_note + interval) % 12)

    return notes

harmony_notes = list(map(notes_for_harmony, harmony))

NOTE_NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']

for note_index in range(0, len(harmony)):
    voice_notes = list(map(lambda note: note % 12, map(lambda voice: voice[note_index], voices)))

    for note in harmony_notes[note_index]:
        if note not in voice_notes:
            print(NOTE_NAMES[note] + ' not present at beat ' + str(note_index + 1))

# 7th resolves downward by step.
# Merge this loop with above loop?
# voice_notes is a repetitive line
for note_index in range(0, len(harmony)):
    voice_notes = list(map(lambda note: note % 12, map(lambda voice: voice[note_index], voices)))

    current_notes = harmony_notes[note_index]

    if len(current_notes) > 3:
        for index, note in enumerate(voice_notes):
            if note == current_notes[3]:
                seventh_voice = index

        if voices[seventh_voice][note_index + 1] - voices[seventh_voice][note_index] not in [-1, -2]:
            print('beat ' + str(note_index + 1) + ' does not have seventh down by step')
            print('expected in ' + VOICE_NAMES[seventh_voice])
