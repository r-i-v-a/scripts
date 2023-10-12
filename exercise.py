#!/usr/bin/env python3

import random

exercises = [
	"Arm circle",
	"Arm curl, w",
	"Back arm wrap",
	"Back core hold",
	"Back twist",
	"Bicycle crunch",
	"Butterfly stretch",
	"Clamshell",
	"Developpe",
	"Downward-facing dog",
	"Front arm wrap",
	"Front core hold",
	"Front plank",
	"Front split",
	"Lunge, w",
	"Modified side plank",
	"Pigeon pose",
	"Plie first",
	"Plie second",
	"Push-up",
	"Quad stretch",
	"Releve, w",
	"Side plank",
	"Side split",
	"Side-angle pose",
	"Sun salutation",
	"Tendu",
	"Toe point and flex",
	"Toe taps",
	"Toe touch",
	"Vertical lift, w",
	"Warrior I",
	"Warrior II",
	"Wheel / bridge",
]

def main():
	i = 1
	while(True):
		input()
		print("{}. {}".format(i, random.choice(exercises)))
		i += 1

if __name__ == "__main__":
    main()
