#!/bin/bash

listTasks () {
	for f in `find . -name "*.txt" -maxdepth 1 -mtime -1`; do
		head -n 1 $f
	done
}

date '+%d/%b/%Y'

cd ~/Documents/__2__/
listTasks

cd ~/Documents/__1__/
listTasks

cd ~/Documents/__h__/
listTasks
