#!/bin/bash

listTasks () {
  for f in `find . -name "*.txt" -maxdepth 1 -mtime -1`; do
    head -n 1 $f
  done
}

date '+%d/%b/%Y'

cd ~/Documents/____/
listTasks

cd ~/Documents/__a__/
listTasks
