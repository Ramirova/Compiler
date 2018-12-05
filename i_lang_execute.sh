#!/bin/bash

python2 Main.py
echo "Starting C code compilation..."
echo ""
gcc c_file.c -w -o exec
echo "C code generation is done!"
./exec $*