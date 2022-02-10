#!/bin/bash

cd ~/Documents/__a__/

printf "\nFinished\n"
for f in [^_]*.txt; do
	head -n 1 $f
done

printf "\nPriority\n"
for f in __*.txt; do
	head -n 1 $f
done

