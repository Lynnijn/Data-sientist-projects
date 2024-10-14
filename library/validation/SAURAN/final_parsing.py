import pandas as pd
import numpy as np
import os

import timezonefinder, pytz

import sys
from pathlib import Path
sys.path.insert(0,str(Path(os.path.abspath('.')).parent.parent))
import library.validation.parsing as parsing


def get_timezone(row):
    tf = timezonefinder.TimezoneFinder()
    timezone_str = tf.certain_timezone_at(lat=row['latitude'], lng=row['longitude'])
    return timezone_str


def final_parse(df, metadata, name):

    columns_ghi = ['GHI_Avg', 'CMP11_2SlrW', 'CMP11_2SlrW_Avg', 'SunWM_Avg', 'MUT_GHI_PSP_34331F3_W_Avg', 'Sol_Global1_Avg']
    columns_dni = ['DNI_Avg', 'CHP1SlrW', 'CHP1SlrW_Avg', 'TrackerWM_Avg', 'MUT_DNI_NIP_31955E6_W_Avg', 'Sol_Direct_Avg']
    columns_dhi = ['DIF_Avg', 'CMP11_1SlrW', 'CMP11_1SlrW_Avg', 'ShadowWM_Avg', 'MUT_DHI_PSP_34332F3_W_Avg', 'Sol_Global2_Avg']
    renaming_dict = {col: 'ghi' for col in columns_ghi}
    renaming_dict.update({col: 'dni' for col in columns_dni})
    renaming_dict.update({col: 'dhi' for col in columns_dhi})
    df.rename(columns=renaming_dict, inplace = True)
    df.columns = df.columns.str.lower()
   

    df = df.apply(pd.to_numeric, errors='coerce')
            
    # remove flatlines
    columns_to_check = ['ghi', 'dni', 'dhi']
    columns_to_apply = [col for col in columns_to_check if col in df.columns]
    for col in columns_to_apply:
        df[col] = parsing.remove_flatlines(df[col])
  
    
    df = df.applymap(lambda x:np.nan if x<0 else x)

    
    start_time = df.first_valid_index()
    end_time = df.last_valid_index()
    df = df.loc[start_time:end_time]
    

    metadata_row = metadata[metadata['station name'] == name]

    if not metadata_row.empty:
        tf = timezonefinder.TimezoneFinder()
        timezone_str = tf.certain_timezone_at(lat=metadata_row["latitude"].values[0], lng=metadata_row["longitude"].values[0])

        df.index = pd.DatetimeIndex(df.index).tz_localize(
            tz=timezone_str,
            ambiguous="NaT",
            nonexistent='shift_forward'
        )

    else:
        print(f"No metadata found for {name}. Skipping this dataframe.")
        
    df.index = df.index.tz_convert('UTC')
        
    return df