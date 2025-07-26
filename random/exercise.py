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
	"clamshell",
	"developpe",
	"downward-facing dog",
	"front arm wrap",
	"front core hold",
	"front plank",
	"front split",
	"lunge | w",
	"modified side plank",
	"pigeon pose",
	"plie first",
	"plie second",
	"push-up",
	"quad stretch",
	"releve | w",
	"side plank",
	"side split",
	"side-angle pose",
	"sun salutation",
	"tendu",
	"toe point and flex",
	"toe taps",
	"toe touch",
	"vertical lift | w",
	"warrior i",
	"warrior ii",
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
