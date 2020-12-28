#!/bin/sh

# 13dx
python ../oucru-13dx/create_data_stacked.py
python ../oucru-13dx/create_data_tidy.py
cp ../oucru-13dx/resources/outputs/13dx-combined-books.csv ./resources/datasets/

# 32dx
#python ../oucru-32dx/create_data_stacked.py
#python ../oucru-32dx/create_data_tidy.py
#cp ../oucru-32dx/resources/outputs/32dx-combined-books.csv ./resources/datasets/

# 42dx
#python ../oucru-42dx/create_data_stacked.py
#python ../oucru-42dx/create_data_tidy.py
#cp ../oucru-42dx/resources/outputs/42dx-combined-books.csv ./resources/datasets/

# 06dx
#python ../oucru-06dx/create_data_stacked.py
#python ../oucru-06dx/create_data_tidy.py
#cp ../oucru-06dx/resources/outputs/06dx-combined-books.csv ./resources/datasets/

# Combine da

#
python combine_data_tidy.py
