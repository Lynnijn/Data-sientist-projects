import pandas as pd
import numpy as np
import os
import pytz

import sys
from pathlib import Path
sys.path.insert(0,str(Path(os.path.abspath('.')).parent.parent))
import library.validation.parsing as parsing



def final_parse(df):
    
    df.columns = df.columns.str.lower()
    
    
    df = df[~df.index.duplicated()]
        
    df = df.applymap(lambda x:np.nan if x<0 else x)
    
    # remove flatlines
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors ='coerce') 
        df[col] = parsing.remove_flatlines(df[col])
    
    start_time = df.first_valid_index()
    end_time = df.last_valid_index()
    df = df.loc[start_time:end_time]
    
    df.index = pd.DatetimeIndex(df.index, tz = pytz.utc)    
    
    return df