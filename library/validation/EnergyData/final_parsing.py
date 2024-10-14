import pandas as pd
import numpy as np
import os
import re

import sys
from pathlib import Path
sys.path.insert(0,str(Path(os.path.abspath('.')).parent.parent))
import library.validation.parsing as parsing
from eee.pandas_util import infer_index_freq



# Renaming columns !
def rename_columns(df, region):
    new_names_count = {'dhi': 0, 'ghi': 0, 'dni': 0, 'dhi_qflag': 0, 'ghi_qflag': 0, 'dni_qflag': 0}
    new_columns = []
    columns = []

    for col in df.columns:
        if 'FLAG' in col:
            if 'DHI' in col:
                new_name = 'dhi_qflag'
            elif 'GHI' in col:
                new_name = 'ghi_qflag'
            elif 'DNI' in col:
                new_name = 'dni_qflag'
            else:
                new_name = col  

            count = new_names_count[new_name] + 1
            new_names_count[new_name] = count

            if count > 1:
                if count == 2: 
                    columns = [f"{region}1_{new_name}" if c == new_name else c for c in columns]
                new_name = f"{region}{count}_{new_name}"
                
        else:
            if 'DHI' in col:
                new_name = 'dhi'
            elif 'GHI' in col:
                new_name = 'ghi'
            elif 'DNI' in col:
                new_name = 'dni'
            else:
                new_name = col  

            count = new_names_count[new_name] + 1
            new_names_count[new_name] = count

            if count > 1:
                if count == 2: 
                    columns = [f"{region}1_{new_name}" if c == new_name else c for c in columns]
                new_name = f"{region}{count}_{new_name}"


        columns.append(new_name)
        new_columns.append(new_name)

    df.columns = columns
    return df



# Convert UTC offsets

def convert_utc_offset(offset_str):
    if offset_str == 'UTC+5.75':       
        return 'Asia/Kathmandu'

    elif offset_str in ['UTC', 'UTC+0']:
        return 'UTC'

    else:
        sign = '+' if '-' in offset_str else '-'
        offset_str = offset_str.replace('UTC', '').replace('+', '').replace('-', '')

        offset_hour = offset_str.split(':')[0]
        
        return f"Etc/GMT{sign}{offset_hour}"



# Change values for flag
def map_values1(value):
    return 2 if value == 0 else 0 if value == 1 else 1

def map_values2(value):
    return 2 if value == 1.00E+02 else 0 if value == 1.00E+00 else 1
    
   
        
   
    
# Final parse

def final_parse(df, normalized_name, name, data):
    
    df = rename_columns(df, normalized_name)
    
    new_column_names = {}
    for col in df.columns:
        if '1_' in col:
            new_col_name = col.split('1_')[1]
            new_column_names[col] = new_col_name
    df.rename(columns=new_column_names, inplace=True)
    
    columns_to_drop = [col for col in df.columns if '2_' in col]
    df.drop(columns=columns_to_drop, inplace=True)
    
    # remove flatlines
    for col in df.columns:
        if not 'qflag' in col:
            df[col] = pd.to_numeric(df[col], errors ='coerce') 
            df[col] = parsing.remove_flatlines(df[col])
    
    df = df[~df.index.duplicated()]
    
    
    # flags
    name_list = ['Hrazdan', 'Masrik', 'Talin', 'YerevanAgro']
    if name in name_list:
        for col in df.columns:
            if 'qflag' in col:
                df[col] = df[col].apply(map_values1)
    

    if name == 'BDFE2 (Feni)' or 'VN' in name or 'LB' in name:      
        for col in df.columns:
            if 'qflag' in col:
                df[col] = df[col].apply(map_values1)
   
        
    df = df.applymap(lambda x:np.nan if x<0 else x)

    
    # remove leading and ending nan
    relevant_columns = [col for col in df.columns if 'qflag' not in col]
    start_time = min(df[col].first_valid_index() for col in relevant_columns)
    end_time = max(df[col].last_valid_index() for col in relevant_columns)
    df = df.loc[start_time:end_time]
    
    
    # datetime
    metadata_row = data[data['station name'] == name]

    if not metadata_row.empty:
        df.index = pd.DatetimeIndex(df.index).tz_localize(
            tz=convert_utc_offset(metadata_row.iloc[0]['time zone'].strip()),
            ambiguous="NaT",
            nonexistent='shift_forward'
        )

    else:
        print(f"No metadata found for {name}. Skipping this dataframe.")
        

        
    # full set
    df = df[~df.index.duplicated()]

    freq_str = str(infer_index_freq(pd.DatetimeIndex(df.index)))
    matches = re.findall(r'(?:(\d+)\s*\*\s*)?(\w+)', freq_str)
    numeric_part, frequency_part = matches[0] if matches[0] else (1, 'Minutes')
    numeric_value = int(numeric_part) if numeric_part and numeric_part.isdigit() else 1
    frequency_value = 'T' if 'Minute' in frequency_part else None

    datarange = pd.date_range(df.index.min(), df.index.max(), freq=f'{numeric_value}{frequency_value}')
    df = df.reindex(datarange)
    
    df.index = df.index.tz_convert('UTC')

    return df