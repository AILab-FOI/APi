#!/bin/bash
shopt -s expand_aliases
source $HOME/.bashrc

case $1 in
    -gg|--grammar-gui)
	antlr4 XMLLexer.g4
	antlr4 APi.g4
	javac APi*.java
	grun APi api_program -gui
    ;;
    -gt|--grammar-tokens)
	antlr4 XMLLexer.g4
	antlr4 APi.g4
	javac APi*.java
	grun APi api_program -tokens
    ;;
    -py|--python)
	antlr4 -Dlanguage=Python3 APi.g4
    ;;
    -r|--run)
	chmod +x APi.py
	./APi.py
    ;;
    -b|--branch)
	if [ $# -eq 1 ]
	then
	    echo "No branch name supplied, aborting!"
	else
	   git checkout -b $2
	fi
    ;;
    -cc|--commit-main)
	if [ $# -eq 1 ]
	then
	    echo "No commit message supplied, aborting!"
	else
	    python3 version_control.py
	    git add .
	    git commit -m "$2"
	    git push origin main
	fi	
    ;;
    -c|--commit)
        if [ $# -eq 2 ]
	then
	    echo "No commit message and/or branch supplied, aborting!"
	else
	    python3 version_control.py
	    git add .
	    git commit -m "$2"
	    git push --set-upstream origin $3
        fi
    ;;
    *)    # unknown option
	echo "Unknown argument, please explain yourself!"
    ;;
esac
