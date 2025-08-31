#!/bin/bash
python3 Predictors/$1.py 
python3 utils/test_predictors.py --predictors $1