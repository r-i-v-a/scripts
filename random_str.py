#!/usr/bin/env python3

import random
import string

characters = string.ascii_letters + string.digits

def main():
	list = []
	for i in range(10):
		list.append(random.choice(characters))
	print(''.join(list))

if __name__ == "__main__":
    main()
