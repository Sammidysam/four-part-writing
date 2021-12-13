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

soprano = []
alto = []
tenor = []
bass = []
harmony = []

with open(input) as input_data:
    # read each line into a variable
