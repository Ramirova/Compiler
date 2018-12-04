#!/bin/bash

python2 main.py
gcc gcc -Wall main.c -o exec
./exec $1, $2, $3 