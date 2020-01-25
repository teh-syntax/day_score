#!/bin/bash
find $1 -type f \( -path node_modules -o -path __pycache__ \) -prune -o -printf '%T@ %p\n' | sort -n | tail -1 | cut -f 1 -d" "
