# four-part-writing
Doing music theory homework automatically through modeling four-part writing as a Constraint Satisfaction Problem

For a description of the project, see the Final Report PDF included
in the repository.

# Running

To run the program, execute `CSP/read_problem.py` with an argument of
the exercise that you hope to run.
For example, you could run `CSP/read_problem.py inputs/Mt1\ partwriting_0001/6.4pw` to run the example that is in the PDF report.
The program will output any validation errors on the output to
stdout (no output means no validation errors) and the filled in example in 4pw format to a file in the local
directory, `temp.4pw`.
While there are multiple solutions for many examples, our program only
outputs one solution at the current time.

If for any example `read_problem.py` outputs the following:

```
Traceback (most recent call last):
  File "/Users/sam/Documents/Programming/artificial-intelligence/four-part-writing/CSP/read_problem.py", line 76, in <module>
    for key in solution:
TypeError: 'NoneType' object is not iterable
```

That just means that a solution can not be found for the 4pw file.
This can come from two cases: either the 4pw file is fully filled in
(no `??`) or there are not any solutions that follow all of our rules.

If you want to run this filled in file through the validator again just
to be certain that there were no validation errors, you could run
`validator/validate.py` with an argument of the filled-in 4pw file
that you seek to validate.
For example, `validator/validate.py temp.4pw`.

If for any example `validate.py` outputs the following:

```
Traceback (most recent call last):
  File "/Users/sam/Documents/Programming/artificial-intelligence/four-part-writing/validator/validate.py", line 48, in <module>
    voices[line_index].append(int(element))
ValueError: invalid literal for int() with base 10: '??'
```

That just means that the 4pw file is not fully filled in.
The validator only runs on fully filled in files.

Some of these errors are uncaught and unhelpful just as this is not
designed to be a general purpose application.
These instructions exist as requested, but in general the application
was designed just to accomplish the research goals of the report,
not to be used by anyone for any purpose (such as actually doing
homework for them).
