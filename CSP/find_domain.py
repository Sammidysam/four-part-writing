# This file contains the function find_domain() which will generate the starting domain for one note of a given line
# with the harmony given as a parameter for context. Also implemented here is the helper function expand_harmony().

import itertools


# This function takes a parameter harmony and returns the pitch content of that chord
# Parameter harmony is a list of the format [root, quality, inversion]
def expand_harmony(harmony):
    pitch_content = []

    # Adding the root
    if harmony[0] == 'A':
        pitch_content.append(10)
    elif harmony[0] == 'B':
        pitch_content.append(11)
    else:
        pitch_content.append(harmony[0])

    root = pitch_content[0]

    # Adding the 3rd
    if harmony[1] in ['M', '7']:
        pitch_content.append((root + 4) % 12)
    elif harmony[1] in ['m', 'b', 'D', 'd']:
        pitch_content.append((root + 3) % 12)

    # Adding the 5th
    if harmony[1] not in ['b', 'D', 'd']:
        pitch_content.append((root + 7) % 12)
    else:
        pitch_content.append((root + 6) % 12)

    # Adding the 7th, if applicable
    if harmony[1] in ['7', 'd']:
        pitch_content.append((root + 10) % 12)
    elif harmony[1] == 'D':
        pitch_content.append((root + 9) % 12)

    return pitch_content


# Generates the starting domain for a note based on the harmony and whether that note is the bass voice
# Parameter harmony is a list of the format [root, quality, inversion]; Parameter is_bass is a bool
def find_domain(harmony, is_bass):
    possible_pitches = expand_harmony(harmony)

    if is_bass:
        inversion = harmony[2]
        if inversion == 'r':
            return list(range(possible_pitches[0], 46, 12))
        else:
            return list(range(possible_pitches[inversion], 46, 12))

    else:
        return list(itertools.chain.from_iterable(list(range(x, 46, 12)) for x in possible_pitches))
