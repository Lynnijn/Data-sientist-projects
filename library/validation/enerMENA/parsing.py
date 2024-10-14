import pandas as pd            
        

def parse(df_p):
    
    df_p.index = pd.to_datetime(df_p['period_end'], format = '%Y-%m-%dT%H:%M:%SZ')
    df_p = df_p[~df_p.index.duplicated()]
    
    # df_p.columns = df_p.columns.str.upper()
    cols_to_keep = ['dhi', 'dni', 'ghi']
    df_p = df_p.loc[:, cols_to_keep]     
    
    datarange = pd.date_range(df_p.first_valid_index(), df_p.last_valid_index(), freq='5T')
    df_p = df_p.reindex(datarange)

    return df_p
