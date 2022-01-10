# This file will handle the reading in of a problem in 4pw format into our CSP model

from constraint import *
from find_domain import find_domain
from rules import generate_constraints
import sys


# Helper function that parses a 3 character harmony string into a len 3 list (e.g. 5Mr -> [5, 'M', 'r'])
def parse_harmony(harmony_string):
    return [int(harmony_string[0]) if harmony_string[0].isdigit() else harmony_string[0], harmony_string[1],
            int(harmony_string[2]) if harmony_string[2].isdigit() else harmony_string[2]]


if len(sys.argv) < 2:
    print('Must provide an input file')
    exit()

file = sys.argv[1]

# Same scheme as in validate.py
voices = [[], [], [], []]
names = ['s', 'a', 't', 'b']  # For variable naming in CSP
ranges = [(24, 45), (19, 38), (12, 33), (0, 24)]  # Pitch ranges for voices
harmony = []

with open(file) as input_data:
    line_index = 0

    for line in input_data:
        stripped = line.rstrip()

        offset = 2 if line_index < 4 else 3

        for i in range(0, len(stripped), offset):
            element = stripped[i:i+offset]

            if line_index < 4:
                voices[line_index].append(int(element) if element.isdigit() else element)
            else:
                harmony.append(parse_harmony(element))

        line_index += 1

problem = Problem()

for i in range(0, 4):
    voice = voices[i]
    name = names[i]
    range_ = ranges[i]

    for j in range(0, len(voice)):
        if voice[j] == '??':  # If note is unknown, add it to the CSP
            variable = name + str(j + 1)
            problem.addVariable(variable, find_domain(harmony[j], i == 3))
            problem.addConstraint(lambda x, w=range_[0], y=range_[1]: w <= x <= y, [variable])  # Add range constraint

            if i > 0:  # Voice crossing constraints upper
                upper_neighbor = voices[i - 1][j]
                upper_name = names[i - 1] + str(j + 1)
                if upper_neighbor == '??':
                    problem.addConstraint(lambda x, y: x < y, [variable, upper_name])
                else:
                    problem.addConstraint(lambda x, y=upper_neighbor: x < y, [variable])
            if i < 3:  # Voice crossing constraints lower
                lower_neighbor = voices[i + 1][j]
                if lower_neighbor != '??':
                    problem.addConstraint(lambda x, y=lower_neighbor: x > y, [variable])

generate_constraints(voices, harmony, problem, names)
print(len(problem.getSolutions()))
