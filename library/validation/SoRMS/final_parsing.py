import pandas as pd
import numpy as np
import os
import re

import sys
from pathlib import Path
sys.path.insert(0,str(Path(os.path.abspath('.')).parent.parent))
import library.validation.parsing as parsing
from eee.pandas_util import infer_index_freq




def final_parse(df, data, name):
    
    # delete columns
    if name == 'NREL Flatirons Campus (M2)':
        df.drop(columns = 'Global (Accumulated) [kWhr/m^2]', inplace = True)
        
    elif name == 'NREL Solar Radiation Research Laboratory (Schott RSP)':
        df.drop(columns = ['Global Horizontal [W/m^2]', 'Direct Normal [W/m^2]', 'Diffuse Horizontal [W/m^2]', 'DHI Correction [W/m^2]'], inplace = True)

    elif name == 'Natural Energy Laboratory of Hawaii Authority (NELHA)':
        df.drop(columns = ['Global UV [W/m^2]', 'Global UV-PFD [umol/s/m^2]', 'Global PAR [umol/s/m^2]'], inplace = True)
        
        
    # rename columns        
    if name == 'Cal Poly Humboldt (SoRMS)':
        column_names = {'Diffuse Horiz (band corr) [W/m^2]': 'cal_poly_humboldt_sorms1_dhi', 
                        'Diffuse Horiz (shadowband) [W/m^2]': 'cal_poly_humboldt_sorms2_dhi', 
                        'Global Horiz [W/m^2]': 'ghi',
                        'Direct Normal (calc) [W/m^2]': 'dni'}        
        
    elif name == 'Elizabeth City State University':
        column_names = {'Diffuse PSP (sband corr) [W/m^2]': 'elizabeth_city_state_university1_dhi', 
                        'Diffuse PSP (sband) [W/m^2]': 'elizabeth_city_state_university2_dhi', 
                        'Global PSP [W/m^2]': 'ghi',
                        'Direct NIP [W/m^2]': 'dni'}    
        
    elif name == 'SOLRMAP University of Arizona (OASIS)':
        column_names = {'Global Horiz (tracker) [W/m^2]': 'solrmap_university_of_arizona_oasis1_ghi', 
                        'Global Horiz (platform) [W/m^2]': 'solrmap_university_of_arizona_oasis2_ghi', 
                        'Diffuse Horiz [W/m^2]': 'dhi',
                        'Direct Normal [W/m^2]': 'dni'} 
        
    else:
        df.columns = df.columns.str.lower()
    
        columns_ghi = df.filter(like = 'global').columns
        columns_dni = df.filter(like = 'direct').columns
        columns_dhi = df.filter(like = 'diffuse').columns
        column_names = {col: 'ghi' for col in columns_ghi}
        column_names.update({col: 'dni' for col in columns_dni})
        column_names.update({col: 'dhi' for col in columns_dhi})
        
    df.rename(columns = column_names, inplace = True)
    
    new_column_names = {}
    for col in df.columns:
        if '1_' in col:
            new_col_name = col.split('1_')[1]
            new_column_names[col] = new_col_name
    df.rename(columns=new_column_names, inplace=True)
    
    columns_to_drop = [col for col in df.columns if '2_' in col]
    df.drop(columns=columns_to_drop, inplace=True)    
    

    # convert to float
    df = df.apply(pd.to_numeric, errors = 'coerce')
   
            
    # remove flatlines
    columns_to_check = ['ghi', 'dni', 'dhi']
    columns_to_apply = [col for col in columns_to_check if col in df.columns]
    for col in columns_to_apply:
        df[col] = parsing.remove_flatlines(df[col])
        
        
        
    # negative
    df = df.applymap(lambda x:np.nan if x<0 else x)

    
    
    # remove leading and ending nan 
    start_time = df.first_valid_index()
    end_time = df.last_valid_index()
    df = df.loc[start_time:end_time]
    
    
    
    # datetime
    metadata_row = data[data['station name'] == name]

    if not metadata_row.empty:
        df.index = pd.DatetimeIndex(df.index).tz_localize(
            tz=metadata_row.iloc[0]['pytz'],
            ambiguous="NaT",
            nonexistent='shift_forward'
    )
  
    else:
        print(f"No metadata found for {name}. Skipping this dataframe.")
        

    
    # Convert the timezone of the datetime index
    df.index = df.index.tz_convert('UTC')
        
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