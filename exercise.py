#!/usr/bin/env python3

import random

exercises = [
	"Arm circle",
	"Arm curl, w",
	"Back arm wrap",
	"Breathing exercises",
	"Butterfly stretch",
	"Downward-facing dog",
	"Extend legs, alternate",
	"Front arm wrap",
	"Front split",
	"Half bridge",
	"Knees to sides, twist",
	"Pigeon pose",
	"Plie first",
	"Plie second",
	"Quad stretch",
	"Releve, w",
	"Side split",
	"Side-angle pose",
	"Stomach on pillow",
	"Tendu",
	"Toe point and flex",
	"Toe taps",
	"Toe touch",
	"Vertical lift, w",
	"Warrior I",
	"Warrior II",
	# "Back core hold",
	# "Back twist",
	# "Bicycle crunch",
	# "Developpe",
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
