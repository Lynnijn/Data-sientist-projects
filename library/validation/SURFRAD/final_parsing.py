import pandas as pd
import numpy as np
import os
import pytz

import sys
from pathlib import Path
sys.path.insert(0,str(Path(os.path.abspath('.')).parent.parent))
import library.validation.parsing as parsing



def final_parse(df):

    # rename columns
    df.columns = df.columns.str.lower()
    column_names = {'flag_ghi': 'ghi_qflag', 'flag_dni': 'dni_qflag', 'flag_dhi': 'dhi_qflag'}
    df.rename(columns=column_names, inplace = True)
    
    # remove flatlines
    columns_to_check = ['ghi', 'dni', 'dhi']
    columns_to_apply = [col for col in columns_to_check if col in df.columns]
    for col in columns_to_apply:
        df[col] = parsing.remove_flatlines(df[col])
       
    
    df = df[~df.index.duplicated()]
        
    # remove negative values
    df = df.applymap(lambda x:np.nan if x<0 else x)

    # remove leading and ending nan
    columns_to_check = ['ghi', 'dni', 'dhi']
    start_time = df[columns_to_check].first_valid_index()
    end_time = df[columns_to_check].last_valid_index()
    df = df.loc[start_time:end_time]

    # datetime index
    df.index = pd.DatetimeIndex(df.index, tz = pytz.utc)    
    
    
    return df