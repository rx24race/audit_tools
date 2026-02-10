# Author: 蔡易儒
# 梯次: 271
# Date: 02/06/2026
# Goal: This is used for deduplicating 業務 files with duplicated SSNs.
# Background: A lot of those 業務 files have duplicated SSNs and are causing issues 
#             when we are going through our auditing processes.
# How-to:
# Run 'python dedupe_tool.py <path to csv file> (including csv extension)'
# Will output to 'dedupe_output' and 'dupes_output'
# 'dedupe_output' includes result set that's deduplicated
# 'dupes_output' includes the duplicated rows that are pre-aggregated

import argparse
import chardet
import pandas as pd

# Example:
# File: resources/94一般役115年3月薪給及主副食費發放清冊2.csv
# Name: 黃千祐
# SSN: N127038313

parser = argparse.ArgumentParser(
    description='Deduplicate the input file based on SSN and write to an output file'
)

parser.add_argument(
    'input_file',
    help='Path to the input file (Currently supports CSV only).'
)

args = parser.parse_args()

output_dir = './dedupe_output'
dupe_dir = './dupes_output'
input_file = args.input_file
dupe_file = dupe_dir + '/' + input_file.split('/')[1].split('.')[0] + '_duplicated.csv'
output_file = output_dir + '/' + input_file.split('/')[1].split('.')[0] + '_deduplicated.csv'

res = None

# opens the input file and detect which encoding it's using
with open(input_file, 'rb') as f:
    res = chardet.detect(f.read())

print('The input file\'s encoding is', res['encoding'])

# read the csv file and load the encoding method dynamically
df = pd.read_csv(input_file, sep=',', encoding=res['encoding'], encoding_errors='replace')
print(df.head(5))

# filter and output out the dupes
dupes = df[df.duplicated('身分證字號', keep=False)]
print(dupes.head(10))
dupes.to_csv(dupe_file, index=False, encoding=res['encoding'], errors='replace')

# aggregate the numeric columns of the duplicated SSNs
df_combined = (
    df.groupby("身分證字號", as_index=False)
      .agg(lambda x: int(x.sum()) if x.dtype.kind in "biufc" else x.iloc[0])
)

print(df_combined.head(5))

# output the final dataframe to the output folder
df_combined.to_csv(output_file, index=False, encoding=res['encoding'], errors='replace')