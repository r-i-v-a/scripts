#!/bin/bash

listTasks () {
  for f in *.txt; do
    head -n 1 $f
  done
}

cd ~/Documents/____/
printf "\nFinished\n"
listTasks

cd ~/Documents/__a__/
printf "\nPriority\n"
listTasks
