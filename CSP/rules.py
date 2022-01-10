from find_domain import expand_harmony


def fulfills_harmony(voices, harmony, problem, names):
    for i in range(0, len(harmony)):
        required_pitches = expand_harmony(harmony[i])
        variables = []
        for j in range(0, 4):
            pitch = voices[j][i]
            if pitch == '??':
                variables.append(names[j] + str(i + 1))  # Keep track of which voices need to be filled
            else:
                try:
                    required_pitches.remove(pitch % 12)  # Keep track of pitches that are already present
                except ValueError:
                    pass

        # Open to suggestions on ways to make this cleaner instead of the multiple elif statements
        if len(variables) == 1:
            problem.addConstraint(lambda x: (x % 12) in required_pitches, [variables[0]])
        elif len(variables) == 2:
            problem.addConstraint(lambda x, y, r=required_pitches: set(r).issubset({x % 12, y % 12}),
                                  [variables[0], variables[1]])
        elif len(variables) == 3:
            problem.addConstraint(lambda x, y, z, r=required_pitches: set(r).issubset({x % 12, y % 12, z % 12}),
                                  [variables[0], variables[1], variables[2]])
        elif len(variables) == 4:
            problem.addConstraint(lambda w, x, y, z, r=required_pitches: set(r).issubset({w % 12, x % 12, y % 12, z % 12}),
                                  [variables[0], variables[1], variables[2], variables[3]])


def parallels(voices, problem, names, interval):
    for i in range(0, len(voices[0]) - 1):  # Doesn't apply to last pitches (final cadence)
        voice_index = 0
        for voice in voices:
            pitch = voice[i]
            pitch_next = voice[i + 1]
            if pitch == '??':
                pitch_variable = names[voice_index] + str(i + 1)
                for j in [x for x in range(0, 4) if x != voice_index]:
                    other_pitch = voices[j][i]
                    other_pitch_next = voices[j][i + 1]
                    if other_pitch == '??':
                        other_pitch_variable = names[j] + str(i + 1)
                        if pitch_next == '??':
                            pitch_next_variable = names[voice_index] + str(i + 2)
                            if other_pitch_next == '??':
                                other_pitch_next_variable = names[j] + str(i + 2)
                                problem.addConstraint(
                                    lambda x1, x2, y1, y2:
                                    not (abs(x1 - y1) % 12 == interval and interval == abs(x2 - y2) % 12 and x1 != x2),
                                    [pitch_variable, pitch_next_variable, other_pitch_variable, other_pitch_next_variable])
                    else:
                        if pitch_next == '??':
                            pitch_next_variable = names[voice_index] + str(i + 2)
                            if other_pitch_next == '??':
                                other_pitch_next_variable = names[j] + str(i + 2)
                                problem.addConstraint(
                                    lambda x1, x2, y2, y1=other_pitch:
                                    not (abs(x1 - y1) % 12 == interval and interval == abs(x2 - y2) % 12 and x1 != x2),
                                    [pitch_variable, pitch_next_variable, other_pitch_next_variable])
                            else:
                                problem.addConstraint(
                                    lambda x1, x2, y1=17, y2=14:
                                    not (abs(x1 - y1) % 12 == interval and interval == abs(x2 - y2) % 12 and x1 != x2),
                                    [pitch_variable, pitch_next_variable])
                # TODO: Implement extended cases
            voice_index += 1


def seventh_resolution(voices, harmony, problem, names):
    for i in range(0, len(harmony)):
        if harmony[i][1] in ['7', 'D', 'd']:
            pitches = expand_harmony(harmony[i])
            voice_index = 0
            for voice in voices:
                if voice[i] == '??':
                    pitch_variable = names[voice_index] + str(i + 1)
                    if voice[i + 1] == '??':
                        pitch_next_variable = names[voice_index] + str(i + 2)
                        problem.addConstraint(lambda x1, x2, ref=pitches[3]:
                                              True if x1 % 12 == ref and (x1 - x2 == 1 or x1 - x2 == 2) else
                                              (True if x1 % 12 != ref else False), [pitch_variable, pitch_next_variable])
                voice_index += 1
                # TODO: Implement the rest of the cases


def generate_constraints(voices, harmony, prob, nam):
    fulfills_harmony(voices, harmony, prob, nam)
    parallels(voices, prob, nam, 7)
    parallels(voices, prob, nam, 12)
    seventh_resolution(voices, harmony, prob, nam)
