#!/bin/bash -l

module add sumo

python sumo_parallel.py 8 1000 --no-interactive > 8_1000_output.txt 2>&1
