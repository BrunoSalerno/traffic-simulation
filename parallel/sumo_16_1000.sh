#!/bin/bash -l

module add sumo

python sumo_parallel.py 16 1000 --no-interactive > 16_1000_output.txt 2>&1
