#!/bin/bash

rm mega.gpx

cat header >> mega.gpx
FILES=geocaches/*
for f in $FILES
do
	echo "Processing $f file..."
	# take action on each file. $f store current file name
	cat $f | tail -n +11 | head -n -1 >> mega.gpx
	echo >> mega.gpx
done
cat footer >> mega.gpx
