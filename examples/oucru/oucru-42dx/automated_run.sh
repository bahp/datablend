#!/bin/sh

# 42dx
python create_data_fixed.py || exit
python create_data_stacked.py || exit
python create_data_tidy.py || exit