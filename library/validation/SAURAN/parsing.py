import pandas as pd
import datetime


def parse_sau(df, cols_to_keep):
    df_full = df.copy()
    
    # Timestamp
    df_full.index = pd.to_datetime(df_full[0])
    
    # Keep columns
    df_full = df_full.loc[:, cols_to_keep]

    # Rename columns
    df_full.columns = ['GHI', 'DNI', 'DHI']
    
    # Remove duplicates
    df_full = df_full[~df_full.index.duplicated(keep='first')]
    
    # Completion
    datarange = pd.date_range(df_full.first_valid_index(), df_full.last_valid_index(), freq='T')
    df_full= df_full.reindex(datarange)

    return df_full