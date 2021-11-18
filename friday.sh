#!/bin/bash

listTasks () {
	for f in *.txt; do
		head -n 1 $f
	done
}

printf "\nFinished\n"
cd ~/Documents/__/
listTasks

printf "\nPriority\n"
cd ~/Documents/__11__/
listTasks
