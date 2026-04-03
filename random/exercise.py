#!/usr/bin/env python3

import random

exercises = [
	"back arm wrap",
	"back core hold",
	"back twist",
	"bicycle crunch",
	"butterfly stretch",
	"cat / cow",
	"clamshell",
	"downward-facing dog",
	"floor barre developpe",
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
	"side leg stretch",
	"side lunge shift",
	"side plank",
	"side split",
	"side-angle pose",
	"small arm circle",
	"small leg circle",
	"standing developpe",
	"sun salutation",
	"tendu",
	"toe point and flex",
	"toe taps",
	"toe touch",
	"turnout rotation",
	"w | arm curl",
	"w | forward press",
	"w | lunge",
	"w | releve",
	"w | renegade row",
	"w | Romanian deadlift",
	"w | single-arm row",
	"w | small arm circle",
	"w | upward press",
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
