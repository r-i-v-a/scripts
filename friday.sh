#!/bin/bash

listTasks () {
	for f in *.txt; do
		head -n 1 $f
	done
}

printf "\nFinished\n"
cd ~/Documents/____/
listTasks

printf "\nPriority\n"
cd ~/Documents/__a__/
listTasks
