#!/bin/bash

python2 main.py
gcc gcc -Wall c_file.c -o exec
./exec $1, $2, $3 