#!/usr/bin/env bash

case $1 in
    -gg|--grammar-gui)
	antlr4 APi.g4
	javac APi*.java
	grun APi api_program -gui
    ;;
    -gt|--grammar-tokens)
	antlr4 APi.g4
	javac APi*.java
	grun APi api_program -tokens
    ;;
    -py|--python)
	antlr -Dlanguage=Python3 APi.g4
    ;;
    -r|--run)
	chmod +x APi.py
	./APi.py
    ;;
    *)    # unknown option
	echo "Unknown argument, please explain yourself!"
    ;;
esac
