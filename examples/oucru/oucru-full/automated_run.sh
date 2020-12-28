#!/bin/sh

# Execute 06dx
python ../oucru-06dx/create_data_fixed.py
python ../oucru-06dx/create_data_stacked.py
python ../oucru-06dx/create_data_tidy.py

# Execute 13dx
python ../oucru-13dx/create_data_fixed.py
python ../oucru-13dx/create_data_stacked.py
python ../oucru-13dx/create_data_tidy.py

# Execute 32dx
python ../oucru-32dx/create_data_fixed.py
python ../oucru-32dx/create_data_stacked.py
python ../oucru-32dx/create_data_tidy.py

# Execute 42dx
python ../oucru-42dx/create_data_fixed.py
python ../oucru-42dx/create_data_stacked.py
python ../oucru-42dx/create_data_tidy.py

# Execute combine data tidy
python combine_data_tidy.py

# Copy
cp ../oucru-06dx/resources/outputs/datasets/06dx_data_tidy.csv ./resources/datasets/
cp ../oucru-13dx/resources/outputs/datasets/13dx_data_tidy.csv ./resources/datasets/
cp ../oucru-32dx/resources/outputs/datasets/32dx_data_tidy.csv ./resources/datasets/
cp ../oucru-42dx/resources/outputs/datasets/42dx_data_tidy.csv ./resources/datasets/