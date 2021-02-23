#!/bin/sh

:'
# Execute 06dx
python ../oucru-06dx/create_data_fixed.py || exit
python ../oucru-06dx/create_data_stacked.py || exit
python ../oucru-06dx/create_data_tidy.py || exit

# Execute 13dx
python ../oucru-13dx/create_data_fixed.py || exit
python ../oucru-13dx/create_data_stacked.py || exit
python ../oucru-13dx/create_data_tidy.py || exit

# Execute 32dx
python ../oucru-32dx/create_data_fixed.py || exit
python ../oucru-32dx/create_data_stacked.py || exit
python ../oucru-32dx/create_data_tidy.py || exit

# Execute 42dx
python ../oucru-42dx/create_data_fixed.py || exit
python ../oucru-42dx/create_data_stacked.py || exit
python ../oucru-42dx/create_data_tidy.py || exit

# Execute md
python ../oucru-md/create_data_fixed.py || exit
python ../oucru-md/create_data_stacked.py || exit
python ../oucru-md/create_data_tidy.py || exit

# Execute dr
python ../oucru-dr/create_data_fixed.py || exit
python ../oucru-dr/create_data_stacked.py || exit
python ../oucru-dr/create_data_tidy.py || exit

# Execute fl
python ../oucru-fl/create_data_fixed.py || exit
python ../oucru-fl/create_data_stacked.py || exit
python ../oucru-fl/create_data_tidy.py || exit

# Execute df
python ../oucru-df/create_data_fixed.py || exit
python ../oucru-df/create_data_stacked.py || exit
python ../oucru-df/create_data_tidy.py || exit

# Execute d001
python ../oucru-d001/create_data_fixed.py || exit
python ../oucru-d001/create_data_stacked.py || exit
python ../oucru-d001/create_data_tidy.py || exit

# Execute 01nva
python ../oucru-01nva/create_data_fixed.py || exit
python ../oucru-01nva/create_data_stacked.py || exit
python ../oucru-01nva/create_data_tidy.py || exit
'

# Linux
:'
# Copy all data tidy
cp ../oucru-06dx/resources/outputs/datasets/06dx_data_tidy_corrected.csv ./resources/datasets/tidy
cp ../oucru-13dx/resources/outputs/datasets/13dx_data_tidy_corrected.csv ./resources/datasets/tidy
cp ../oucru-32dx/resources/outputs/datasets/32dx_data_tidy_corrected.csv ./resources/datasets/tidy
cp ../oucru-42dx/resources/outputs/datasets/42dx_data_tidy_corrected.csv ./resources/datasets/tidy
cp ../oucru-md/resources/outputs/datasets/md_data_tidy_corrected.csv ./resources/datasets/tidy
cp ../oucru-dr/resources/outputs/datasets/dr_data_tidy_corrected.csv ./resources/datasets/tidy
cp ../oucru-fl/resources/outputs/datasets/fl_data_tidy_corrected.csv ./resources/datasets/tidy
cp ../oucru-df/resources/outputs/datasets/df_data_tidy_corrected.csv ./resources/datasets/tidy
cp ../oucru-d001/resources/outputs/datasets/d001_data_tidy_corrected.csv ./resources/datasets/tidy
cp ../oucru-01nva/resources/outputs/datasets/01nva_data_tidy_corrected.csv ./resources/datasets/tidy

# Copy all data stacked
cp ../oucru-06dx/resources/outputs/datasets/06dx_data_stacked_corrected.csv ./resources/datasets/stacked
cp ../oucru-13dx/resources/outputs/datasets/13dx_data_stacked_corrected.csv ./resources/datasets/stacked
cp ../oucru-32dx/resources/outputs/datasets/32dx_data_stacked_corrected.csv ./resources/datasets/stacked
cp ../oucru-42dx/resources/outputs/datasets/42dx_data_stacked_corrected.csv ./resources/datasets/stacked
cp ../oucru-md/resources/outputs/datasets/md_data_stacked_corrected.csv ./resources/datasets/stacked
cp ../oucru-dr/resources/outputs/datasets/dr_data_stacked_corrected.csv ./resources/datasets/stacked
cp ../oucru-fl/resources/outputs/datasets/fl_data_stacked_corrected.csv ./resources/datasets/stacked
cp ../oucru-df/resources/outputs/datasets/df_data_stacked_corrected.csv ./resources/datasets/stacked
cp ../oucru-d001/resources/outputs/datasets/d001_data_stacked_corrected.csv ./resources/datasets/stacked
cp ../oucru-01nva/resources/outputs/datasets/01nva_data_stacked_corrected.csv ./resources/datasets/stacked
'

# Windows

# Copy all data tidy
xcopy ..\\oucru-06dx\\resources\\outputs\\datasets\\06dx_data_tidy_corrected.csv .\\resources\\datasets\\tidy
xcopy ..\\oucru-13dx\\resources\\outputs\\datasets\\13dx_data_tidy_corrected.csv .\\resources\\datasets\\tidy
xcopy ..\\oucru-32dx\\resources\\outputs\\datasets\\32dx_data_tidy_corrected.csv .\\resources\\datasets\\tidy
xcopy ..\\oucru-42dx\\resources\\outputs\\datasets\\42dx_data_tidy_corrected.csv .\\resources\\datasets\\tidy
xcopy ..\\oucru-md\\resources\\outputs\\datasets\\md_data_tidy_corrected.csv .\\resources\\datasets\\tidy
xcopy ..\\oucru-dr\\resources\\outputs\\datasets\\dr_data_tidy_corrected.csv .\\resources\\datasets\\tidy
xcopy ..\\oucru-fl\\resources\\outputs\\datasets\\fl_data_tidy_corrected.csv .\\resources\\datasets\\tidy
xcopy ..\\oucru-df\\resources\\outputs\\datasets\\df_data_tidy_corrected.csv .\\resources\\datasets\\tidy
xcopy ..\\oucru-d001\\resources\\outputs\\datasets\\d001_data_tidy_corrected.csv .\\resources\\datasets\\tidy
xcopy ..\\oucru-01nva\\resources\\outputs\\datasets\\01nva_data_tidy_corrected.csv .\\resources\\datasets\\tidy

# Copy all data stacked
xcopy ..\\oucru-06dx\\resources\\outputs\\datasets\\06dx_data_stacked_corrected.csv .\\resources\\datasets\\stacked
xcopy ..\\oucru-13dx\\resources\\outputs\\datasets\\13dx_data_stacked_corrected.csv .\\resources\\datasets\\stacked
xcopy ..\\oucru-32dx\\resources\\outputs\\datasets\\32dx_data_stacked_corrected.csv .\\resources\\datasets\\stacked
xcopy ..\\oucru-42dx\\resources\\outputs\\datasets\\42dx_data_stacked_corrected.csv .\\resources\\datasets\\stacked
xcopy ..\\oucru-md\\resources\\outputs\\datasets\\md_data_stacked_corrected.csv .\\resources\\datasets\\stacked
xcopy ..\\oucru-dr\\resources\\outputs\\datasets\\dr_data_stacked_corrected.csv .\\resources\\datasets\\stacked
xcopy ..\\oucru-fl\\resources\\outputs\\datasets\\fl_data_stacked_corrected.csv .\\resources\\datasets\\stacked
xcopy ..\\oucru-df\\resources\\outputs\\datasets\\df_data_stacked_corrected.csv .\\resources\\datasets\\stacked
xcopy ..\\oucru-d001\\resources\\outputs\\datasets\\d001_data_stacked_corrected.csv .\\resources\\datasets\\stacked
xcopy ..\\oucru-01nva\\resources\\outputs\\datasets\\01nva_data_stacked_corrected.csv .\\resources\\datasets\\stacked

# Execute combine data tidy
python combine_data.py || exit

# Execute report features
python report.py || exit

:'
# Create HTML profiles
python report_profile_html.py || exit
'