#!/usr/bin/env python3

import random

exercises = [
	"Arm circle",
	"Arm curl, w",
	"Back arm wrap",
	"Back core hold",
	"Back twist",
	"Bicycle crunch",
	"Developpe",
	"Front arm wrap",
	"Front core hold",
	"Front split",
	"Full bridge",
	"Half bridge",
	"Lunge, w",
	"Plie first",
	"Plie second",
	"Push-up",
	"Quad stretch",
	"Rear lift, w",
	"Releve, w",
	"Side split",
	"Sun salutation",
	"Tendu",
	"Toe touch",
	"Turnout squat",
	"Vertical lift, w"
]

def main():
	i = 1
	while(True):
		input()
		print("{}. {}".format(i, random.choice(exercises)))
		i += 1

if __name__ == "__main__":
    main()

