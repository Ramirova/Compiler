#!/bin/bash

python2 antlr.py
gcc -Wall c_file.c -o exec
./exec $*