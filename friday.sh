#!/bin/bash

listTasks () {
	for f in *.txt; do
		head -n 1 $f
	done
}

cd ~/Documents/__2__/
printf "\nDone\n"
listTasks

cd ~/Documents/__1__/
printf "\nIn Progress\n"
listTasks

cd ~/Documents/__h__/
printf "\nOn Hold\n"
listTasks
