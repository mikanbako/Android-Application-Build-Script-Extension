#!/bin/bash

# Run test about Python scripts.

CURRENT_DIRECTORY=`pwd`
TOP_DIRECTORY=`dirname $CURRENT_DIRECTORY`

export PYTHONPATH=$TOP_DIRECTORY/subscripts

./test_validate_test_text_result.py

