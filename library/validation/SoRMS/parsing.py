import pandas as pd
import datetime


def parse_rms(df, freq='T'):
    df_full = df.copy()
    
    # Index 
    DateTime = pd.to_datetime(df_full.iloc[:,0] + ' ' + df_full.iloc[:,1],errors='coerce')
    df_full.index = DateTime
    df_full = df_full.loc[df_full.index.dropna()]

    
    # Keep columns
    df_full = df_full.drop(df_full.iloc[:, 0:2], axis=1)
    
    # full set
    df_full = df_full[~df_full.index.duplicated(keep='first')]
    
    datarange = pd.date_range(df_full.first_valid_index(), df_full.last_valid_index(), freq=freq)
    df_full = df_full.reindex(datarange)
        
    return df_full