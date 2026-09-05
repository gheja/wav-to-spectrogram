#!/bin/bash

if [ $# != 1 ]; then
	echo "$0 <input_file>"
	exit 1
fi

input_file=`readlink -f -- "$1"`
script_dir="$(dirname -- $(readlink -f -- "${BASH_SOURCE[0]}"))"

cd "$script_dir"

. .venv/bin/activate

python3 src/quick_create.py "$input_file"
