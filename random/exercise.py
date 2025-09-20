#!/usr/bin/env python3

import random

exercises = [
	"arm circle",
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
	"front leg stretch",
	"front plank",
	"front split",
	"hundred",
	"kick back",
	"mermaid side stretch",
	"modified side plank",
	"pigeon pose",
	"plie first",
	"plie second",
	"push-up",
	"quad stretch",
	"side plank",
	"side split",
	"side-angle pose",
	"small leg circle",
	"sun salutation",
	"tendu",
	"toe point and flex",
	"toe taps",
	"toe touch",
	"w | arm curl",
	"w | front arm lift",
	"w | releve",
	"w | side arm lift",
	"w | vertical arm lift",
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
