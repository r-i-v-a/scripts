#!/bin/bash

listTasks () {
  for f in *.txt; do
    head -n 1 $f
  done
}

cd ~/Documents/__X__/
printf "\nDone\n"
listTasks

cd ~/Documents/__1__/
printf "\nDo Next\n"
listTasks
