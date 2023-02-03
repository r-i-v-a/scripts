#!/usr/bin/env python3

import random

exercises = [
	"Arm circle",
	"Arm curl, w",
	"Back arm wrap",
	"Back twist",
	"Butterfly stretch",
	"Clamshell",
	"Developpe",
	"Downward-facing dog",
	"Front arm wrap",
	"Front split",
	"Half bridge",
	"Modified side plank",
	"Pigeon pose",
	"Plie first",
	"Plie second",
	"Quad stretch",
	"Releve, w",
	"Side split",
	"Side-angle pose",
	"Tendu",
	"Toe point and flex",
	"Toe taps",
	"Toe touch",
	"Vertical lift, w",
	"Warrior I",
	"Warrior II",
	# "Back core hold",
	# "Bicycle crunch",
	# "Front core hold",
	# "Front plank",
	# "Full bridge",
	# "Lunge, w",
	# "Push-up",
	# "Side plank",
	# "Sun salutation",
]

def main():
	i = 1
	while(True):
		input()
		print("{}. {}".format(i, random.choice(exercises)))
		i += 1

if __name__ == "__main__":
    main()
