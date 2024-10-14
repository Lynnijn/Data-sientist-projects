import pandas as pd            
        


def parse(data_file_path, file, df_p, DateTime, freq = 'T'):
    df_p.index = pd.to_datetime(DateTime)
    df_p = df_p[~df_p.index.duplicated()]
    
    df_p.columns = df_p.columns.str.upper()
    df_p = df_p[df_p.columns[df_p.columns.str.contains('GHI|DNI|DHI')]]
        
    datarange = pd.date_range(df_p.first_valid_index(), df_p.last_valid_index(), freq=freq)
    df_p = df_p.reindex(datarange)

    return df_p




# def read(data_file_path, file, dfs):    
    

#     if 'bangladesh' in file or 'vietnam' in file or 'lebanon' in file:
#         df = pd.read_csv(data_file_path, skiprows = 1)
        
#     file_list = ['benin', 'burkinafaso', 'cotedivoire', 'gambia', 'ghana', 'guinea', 'liberia', 'mali', 'nigeria', 'niger', 'measurements_senegal', 'sierraleone', 'togo']
#     elif any (fi in file for fi in file_list):
#         df = pd.read_csv(data_file_path, encoding='ISO-8859-1', header=0, skiprows=[1])
        
#     elif file.startswith('solar-measurementssenegal-'):
#         df = pd.read_csv(data_file_path, sep = ';')
        
#     else:
#         df = pd.read_csv(data_file_path)    
        
        
#     if 'year' in file:
#         place = file.split('_')[1]
#         key = f'{place}'

#         if key in dfs:
#             # dfs[key] = pd.concat([dfs[key], df], ignore_index=True)
#             return pd.concat([dfs[key], df], ignore_index=True)

#         else:
#             dfs[key] = df.copy()
            
#     else:
#         return df
 
    
    
# def read(data_file_path, file, skiprows = None, encoding = 'utf-8', sep = ','):    
    
#     df = pd.read_csv(data_file_path, skiprows = skiprows, encoding = encoding, sep = sep)




# def parse(data_file_path, file, df_p, DateTime, freq = 'T'):
    
#     if '10min' in file:
#         df_p = df.copy()
    
#         df_p = df_p.rename(columns={'#year': 'year'})
#         df_p.index = pd.to_datetime(df_p[['year', 'month', 'day', 'hour', 'minute']])

#         df_p.columns = df_p.columns.str.upper()
#         df_p = df_p[df_p.columns[df_p.columns.str.contains('GHI|DNI|DNI')]]
        
#         datarange = pd.date_range(df_p.first_valid_index(), df_p.last_valid_index(), freq='10T')
#         df_p = df_p.reindex(datarange)
        
        
#     elif 'pakistan' in file:
#         df_p = df.copy()
        
#         df_p.columns = df_p.columns.str.upper()
    
#         df_p.index = pd.to_datetime(df_p[df_p.filter(like='TIME').columns[0]])

#         df_p = df_p[df_p.columns[df_p.columns.str.contains('GHI|DNI|DNI')]]
        
#         datarange = pd.date_range(df_p.first_valid_index(), df_p.last_valid_index(), freq='10T')
#         df_p = df_p.reindex(datarange)
        
        
        
#     else:
#         df_p = df.copy()
        
#         df_p.columns = df_p.columns.str.upper()
    
#         df_p.index = pd.to_datetime(df_p[df_p.filter(like='TIME').columns[0]])

#         df_p = df_p[df_p.columns[df_p.columns.str.contains('GHI|DNI|DNI')]]
        
#         datarange = pd.date_range(df_p.first_valid_index(), df_p.last_valid_index(), freq='T')
#         df_p = df_p.reindex(datarange)
        
#     return df_p
