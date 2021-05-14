#!/bin/bash

#TU
python3 -m pytest --junitxml build/results_tu_spot.xml tests/tu/spot_tests.py -vxk "not test_compute_side"
python3 -m pytest --junitxml build/results_tu_futures.xml tests/tu/futures_tests.py -vxk "not test_compute_side"

#TV