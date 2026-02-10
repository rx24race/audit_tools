# Author: 蔡易儒
# 梯次: 271
# Date: 02/09/2026
# Goal: When calculating monthly pensions, we need to combine all the files
#       we have for the previous month, and it's been all manual. Therefore,
#       this tool will help us with automation.
#
# Good to know:
# 1. Double check excel files are in CSV. This tool will not work for other file extensions
# 2. Make sure excel files do not have unnecessary summation lines at the end
#
# How to:
# 1. Drop all the files from previous month (改服, 補發, 大宗, 新梯) into the 'resources' folder
#    So for example, if i'm working on 11510 pensions, i'd include all the files from October, 115.
# 2. Run 'python pension_tool.py' in command line and the results will be outputted to 'output' folder
# 3. 'output_自提' is for 自提, 'output_公提' is for 公提.

import os
import pandas as pd
import chardet

# columns to extract:
# 姓名
# 身分證字號
# (代扣)自提退休金金額
# 單位負擔退休金金額

folder_path = 'pension_resources'
output_path = 'pension_output'
encoding_method = 'Big5'


# This is to check encoding methods for all the input files to make sure
# they are the same encoding methods.
def check_encoding():
    global encoding_method
    res = None
    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.csv'):
                file_path = os.path.join(folder_path, filename)

                with open(file_path, 'rb') as f:
                    res = chardet.detect(f.read())
                
                print(file_path + ' ' + res['encoding'])
                if res['encoding'] != encoding_method:
                    raise ValueError('The encoding methods are not the same')
                
                encoding_method = res['encoding']

        print('All CSV files have the same encoding: ' + res['encoding'])
        print('******************************************')

    except Exception as e:
        print('Encoding validation failed')
        print(e)    


# Combine all the entries for each SSN along with interested columns only.
def get_combined_csv_files():
    columns = [
        '姓名',
        '身分證字號',
        '(代扣)自提退休金金額',
        '單位負擔退休金金額'
    ]

    # files without 單位負擔退休金金額 column
    trimmed_columns = [
        '姓名',
        '身分證字號',
        '(代扣)自提退休金金額'
    ]

    df_combined = pd.DataFrame(columns=columns)
    print(df_combined)

    dfs = []

    try:
        for filename in os.listdir(folder_path):
            is_changed = False
            file_path = os.path.join(folder_path, filename)

            df_temp = pd.read_csv(file_path, sep=',', encoding=encoding_method, encoding_errors='replace')
            print(f'Current file {file_path}')

            missing = None

            if '單位負擔退休金金額' not in df_temp.columns:
                print('This file is missing govt column')
                missing = set(trimmed_columns) - set(df_temp.columns)
                is_changed = True
            else:
                missing = set(columns) - set(df_temp.columns)

            if missing:
                raise ValueError(f'Missing columns: {missing}')
            else:
                print('All columns are present.')
    
            # manually add the missing column
            if is_changed:
                df_temp['單位負擔退休金金額'] = 0

            df_temp = df_temp[columns]
            print(df_temp.head(10))
            dfs.append(df_temp)

        df_combined = pd.concat(dfs, ignore_index=True)
        print(df_combined.head(10))
        return df_combined
        
    except Exception as e:
        print('Error in processing file')
        print(e)


# Aggregate all the duplicated SSNs
def aggregate_combined_df(df_combined):
    try:
        df_agg = (
            df_combined.groupby("身分證字號", as_index=False)
            .agg(lambda x: int(x.sum()) if x.dtype.kind in "biufc" else x.iloc[0])
        )
    
    except Exception as e:
        print('Error when aggregating data')
        print(e)

    # filter out the 0s for both
    df_agg_self = df_agg[(df_agg['(代扣)自提退休金金額'] != 0)]
    df_agg_self = df_agg_self[['姓名', '身分證字號', '(代扣)自提退休金金額']]
    print(df_agg_self.dtypes)
    df_agg_govt = df_agg[(df_agg['單位負擔退休金金額'] != 0)]
    df_agg_govt = df_agg_govt[['姓名', '身分證字號', '單位負擔退休金金額']]
    print(df_agg_govt.dtypes)
    return df_agg_self, df_agg_govt


def write_to_csv(df, type):
    df.to_csv(f'./{output_path}/output_{type}.csv', index=False, encoding=encoding_method, errors = 'replace')


check_encoding()
df_combined = get_combined_csv_files()
df_agg_self, df_agg_govt = aggregate_combined_df(df_combined)
write_to_csv(df_agg_self, '自提')
write_to_csv(df_agg_govt, '公提')