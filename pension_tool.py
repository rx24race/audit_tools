# Author: 蔡易儒
# 梯次: 271
# Date: 02/09/2026
# Goal: When calculating monthly pensions, we need to combine all the files
#       we have for the previous month, and it's been all manual. Therefore,
#       this tool will help us with automation.

import os
import pandas as pd
import argparse
import chardet

# columns to extract:
# 姓名
# 身分證字號
# (代扣)自提退休金金額
# 單位負擔退休金金額

folder_path = 'resources'
encoding_method = 'Big5'

def check_encoding():
    global encoding_method
    res = None
    try:
        for filename in os.listdir(folder_path):
            if filename.lower().endswith('.csv'):
                file_path = os.path.join(folder_path, filename)

                with open(file_path, 'rb') as f:
                    res = chardet.detect(f.read())
                
                # print(file_path + ' ' + res['encoding'])
                if res['encoding'] != encoding_method:
                    raise ValueError('The encoding methods are not the same')
                
                encoding_method = res['encoding']

        print('All CSV files have the same encoding: ' + res['encoding'])
        print('******************************************')

    except Exception as e:
        print('Encoding validation failed')
        print(e)    


def get_combined_csv_files():
    columns = [
        '姓名',
        '身分證字號',
        '(代扣)自提退休金金額',
        '單位負擔退休金金額'
    ]

    # 改服用的
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
            if '改補' in file_path:
                missing = set(trimmed_columns) - set(df_temp.columns)
                is_changed = True
            else:
                missing = set(columns) - set(df_temp.columns)

            if missing:
                raise ValueError(f'Missing columns: {missing}')
    
            if is_changed:
                df_temp['單位負擔退休金金額'] = 0

            df_temp = df_temp[columns]
            dfs.append(df_temp)

        df_combined = pd.concat(dfs, ignore_index=True)
        print(df_combined.head(10))
        return df_combined
        
    except Exception as e:
        print('Error in processing file')
        print(e)


def aggregate_combined_df(df_combined):
    df_agg = (
        df_combined.groupby("身分證字號", as_index=False)
        .agg(lambda x: int(x.sum()) if x.dtype.kind in "biufc" else x.iloc[0])
    )

    df_agg = df_agg[(df_agg['(代扣)自提退休金金額'] != 0) | (df_agg['單位負擔退休金金額'] != 0)]
    return df_agg


def write_to_csv(df):
    df.to_csv('./output/test_output.csv', index=False, encoding=encoding_method, errors = 'replace')


check_encoding()
df_combined = get_combined_csv_files()
df_combined_agg = aggregate_combined_df(df_combined)
write_to_csv(df_combined_agg)