#!/bin/bash
#install tulip plugin


DIRECTORY="/Applications/Tulip-4.7.0.app";

if [ -z "$1" ]; 
	then echo "path to Tulip is unset, using '$DIRECTORY"; 
	else
		DIRECTORY=$1 
		echo "path to Tulip is '$1'"; 
fi;

if [ -d "$DIRECTORY" ]; 
	then 

		if [ -z "$2" ]; then
			if [ "$(uname)" == "Darwin" ]; then
			    DIRECTORY=$DIRECTORY"/Contents/lib/tulip/python";        
				echo "OSX detected, path to lib is '$DIRECTORY";
			elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
			    DIRECTORY=$DIRECTORY"/lib/tulip/python";
				echo "Linux detected, path to lib is '$DIRECTORY";
			elif [ "$(expr substr $(uname -s) 1 5)" == "MINGW" ]; then
			    DIRECTORY=$DIRECTORY"/lib/tulip/python";
				echo "MINGW detected, path to lib is '$DIRECTORY";
			else
				DIRECTORY=$DIRECTORY"/lib/tulip/python";
				echo "OS undetected using linux default, path to lib is '$DIRECTORY";
			fi;
		else
			DIRECTORY=$DIRECTORY$2;
			echo "Path to lib/python manually set, now is '$DIRECTORY";
		fi;

	else 
		echo "path to Tulip, '$DIRECTORY', is not valid";
		exit 1;
fi;

if ! [ -d "$DIRECTORY" ]; then
	mkdir $DIRECTORY
	echo "creating the directory $DIRECTORY"
fi;

echo "copying the python files: "
for f in ${PWD}/*.py;
do
	if [[ $f =~ \.py$ ]]; then
		echo "copying '$f to $DIRECTORY"
		cp $f $DIRECTORY
	fi;
	
done
#cp *.py $DIRECTORY
echo "done"
exit