#!/bin/bash

listTasks () {
  for f in *.txt; do
    head -n 1 $f
  done
}

cd ~/Documents/__X__/
printf "\nFinished\n"
listTasks

cd ~/Documents/__I__/
printf "\nPriority I\n"
listTasks

cd ~/Documents/__II__/
printf "\nPriority II\n"
listTasks
