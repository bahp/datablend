# Libraries
import ast
import collections
import pandas as pd


# -----------------
# Methods
# -----------------
def invert(d):
    if isinstance(d, dict):
        return {v: k for k, v in d.items()}
    return d


def str2eval(x):
    if pd.isnull(x):
        return None
    return ast.literal_eval(x)


def sortkeys(d):
    if isinstance(d, dict):
        return collections.OrderedDict(sorted(d.items()))
    return d

codes = ['06dx', '13dx', '32dx', '42dx', 'md']

path = "../oucru-{0}/resources/outputs/"
path += "templates/ccfgs_{1}_data_fixed.xlsx"

# Loop
for c in codes:

    # Create path
    path_tmp = path.format(c, c)

    # Read excel
    sheets = pd.read_excel(path_tmp, sheet_name=None)

    # Loop
    for sheet, df in sheets.items():
        df.to_replace = df.to_replace.apply(str2eval)
        df.to_replace = df.to_replace.apply(invert)
        #df.to_replace = df.to_replace.apply(sortkeys)

    # Create fullpath
    fullpath = path_tmp.replace('.xlsx', '_inverted.xlsx')

    # Creating Excel Writer Object from Pandas
    writer = pd.ExcelWriter(fullpath, engine='xlsxwriter')

    # Save each frame
    for sheet, frame in sheets.items():
        frame.to_excel(writer, sheet_name=sheet, index=False)

    # critical last step
    writer.save()