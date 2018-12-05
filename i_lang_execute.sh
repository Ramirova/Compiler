#!/bin/bash

python2 Main.py
gcc c_file.c -w -o exec
./exec $*