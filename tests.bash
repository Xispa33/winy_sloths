#!/bin/bash

export PYTHONPATH=$PWD

#TU
python3 -m pytest --junitxml tests/results/tu_spot.xml tests/tu/spot_tests.py -vxk "not test_compute_side"
python3 -m pytest --junitxml tests/results/tu_futures.xml tests/tu/futures_tests.py -vxk "not test_compute_side"
rm .coverage.cloud*

#TV
coverage run -m pytest --junitxml tests/results/tv_spot.xml tests/tv/spot_tests.py -vxk "not test_compute_side"
coverage run -m pytest --junitxml tests/results/tv_futures.xml tests/tv/futures_tests.py -vxk "not test_compute_side"
coverage combine; coverage report
rm .coverage