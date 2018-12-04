#!/bin/bash

python2 Main.py
gcc -Wall c_file.c -o exec
./exec $*