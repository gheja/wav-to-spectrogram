#!/bin/bash

if [ $# != 1 ]; then
	echo "$0 <input_file>"
	exit 1
fi

input_file=`readlink -f "$1"`

cd /home/gheja/works_local/wav-to-spectrogram || exit 1

. .venv/bin/activate

python3 src/quick_create.py "$input_file"
