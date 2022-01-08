#!/usr/bin/env python3

import random

exercises = [
	"A",
	"B",
	"C",
	"D",
	"E"
]

def main():
	i = 1
	while(True):
		input()
		print("{}. {}".format(i, random.choice(exercises)))
		i += 1

if __name__ == "__main__":
    main()

