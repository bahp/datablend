#!/bin/sh

# 13dx
python create_data_fixed.py || exit
python create_data_stacked.py || exit
python create_data_tidy.py || exit