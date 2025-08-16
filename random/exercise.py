#!/usr/bin/env python3

import random

exercises = [
	"arm circle",
	"arm curl | r",
	"back arm wrap",
	"back core hold",
	"back twist",
	"bicycle crunch",
	"butterfly stretch",
	"clamshell | r",
	"developpe",
	"downward-facing dog",
	"front arm wrap",
	"front core hold",
	"front leg stretch | s",
	"front plank",
	"front split",
	"hundred",
	"kick back",
	"mermaid side stretch",
	"modified side plank",
	"one side arm pull-down | r",
	"pigeon pose",
	"plie first",
	"plie second",
	"push-up",
	"quad stretch",
	"releve | r",
	"seated rowing | r",
	"side leg circles | r",
	"side leg stretch | s",
	"side plank",
	"side split",
	"side-angle pose",
	"sun salutation",
	"symmetrical arm pull-down | r",
	"tendu",
	"toe point and flex",
	"toe taps",
	"toe touch",
	"vertical lift | r",
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
