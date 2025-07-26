#!/usr/bin/env python3

import random

exercises = [
	"arm circle",
	"arm curl | w",
	"back arm wrap",
	"back core hold",
	"back twist",
	"bicycle crunch",
	"butterfly stretch",
	"clamshell | b",
	"developpe",
	"downward-facing dog",
	"front arm wrap",
	"front core hold",
	"front leg circles | b",
	"front plank",
	"front split",
	"hundred",
	"lunge | w",
	"mermaid side stretch",
	"modified side plank",
	"one side arm pull-down | b",
	"pigeon pose",
	"plie first",
	"plie second",
	"push-up",
	"quad stretch",
	"releve | w",
	"seated rowing | b",
	"side leg circles | b",
	"side plank",
	"side split",
	"side-angle pose",
	"sun salutation",
	"symmetrical arm pull-down | b",
	"tendu",
	"toe point and flex",
	"toe taps",
	"toe touch",
	"vertical lift | w",
	"warrior I",
	"warrior II",
	"wheel / bridge",
]

def main():
	i = 1
	while(True):
		input()
		print("{}. {}".format(i, random.choice(exercises)))
		i += 1

if __name__ == "__main__":
    main()
