#!/bin/bash

listTasks () {
  for f in `find . -name "*.txt" -maxdepth 1 -mtime -1`; do
    head -n 1 $f
  done
}

date '+%d/%b/%Y'

cd ~/Documents/__X__/
listTasks

cd ~/Documents/__I__/
listTasks

cd ~/Documents/__II__/
listTasks
