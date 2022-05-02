#!/usr/bin/env python3

import random

exercises = [
	"Arm circle",
	"Arm curl, w",
	"Back arm wrap",
	"Breathing exercises",
	"Butterfly stretch",
	"Extend legs, alternate",
	"Front arm wrap",
	"Front split",
	"Half bridge",
	"Knees to sides",
	"Knees to sides, twist",
	"Plie first",
	"Plie second",
	"Quad stretch",
	"Rear lift, w",
	"Releve, w",
	"Tendu",
	"Toe point and flex",
	"Toe touch",
	"Vertical lift, w",
	# "Back core hold",
	# "Back twist",
	# "Bicycle crunch",
	# "Developpe",
	# "Front core hold",
	# "Full bridge",
	# "Lunge, w",
	# "Push-up",
	# "Side split",
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
