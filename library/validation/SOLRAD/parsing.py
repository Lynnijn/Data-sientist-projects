import pandas as pd
import datetime


# def parse(df, sep1 = '2014-12-31 23:57:00', sep2 = '2014-12-31 23:57:00', end = '2023-11-08 23:59:00'):
#     df_full = df.copy()
    
#     # Timestamp
#     DateTime = df_full[[0, 2, 3, 4, 5]].apply(lambda s : datetime.datetime(*s),axis = 1)
#     df_full.index = DateTime
    
#     # Keep columns
#     cols_to_keep = [8,9,10,11,12,13]
#     df_full = df_full.loc[:, cols_to_keep]

#     # Rename columns
#     df_full.columns = ['GHI', 'flag_GHI', 'DNI', 'flag_DNI', 'DHI', 'flag_DHI']
  
#     # Separate
#     df_3m = df_full.loc['2005-01-01 00:00:00':sep1]
#     df_1m = df_full[~df_full.index.isin(df_3m.index)]

#     # Completion
#     datarange_3m = pd.date_range('2005-01-01 00:00:00', sep1, freq='3T')
#     df_3m_merged = pd.merge(df_3m, pd.DataFrame(index = datarange_3m),right_index=True,left_index=True,how='outer')
#     df_3m_co = df_3m_merged.fillna(value={'GHI': -9999.9, 'DNI': -9999.9, 'DHI': -9999.9, 'flag_GHI': 1, 'flag_DNI': 1, 'flag_DHI': 1})
#     df_3m_co[['flag_GHI', 'flag_DNI', 'flag_DHI']] = df_3m_co[['flag_GHI', 'flag_DNI', 'flag_DHI']].astype(int)

#     datarange_1m = pd.date_range(sep2, end, freq='T')
#     df_1m_merged = pd.merge(df_1m, pd.DataFrame(index = datarange_1m),right_index=True,left_index=True,how='outer')
#     df_1m_co = df_1m_merged.fillna(value={'GHI': -9999.9, 'DNI': -9999.9, 'DHI': -9999.9, 'flag_GHI': 1, 'flag_DNI': 1, 'flag_DHI': 1})
#     df_1m_co[['flag_GHI', 'flag_DNI', 'flag_DHI']] = df_1m_co[['flag_GHI', 'flag_DNI', 'flag_DHI']].astype(int)

#     return df_3m_co, df_1m_co

def parse(df, sep1='2014-12-31 23:57:00', sep2='2014-12-31 23:57:00', end = '2023-11-08 23:59:00'):
    # Timestamp
    DateTime = df[[0, 2, 3, 4, 5]].apply(lambda s: datetime.datetime(*s), axis=1)
    df.index = DateTime

    # Keep columns
    cols_to_keep = [8,9,10,11,12,13]
    df = df.iloc[:, cols_to_keep]

    # Rename columns
    df.columns = ['GHI', 'flag_GHI', 'DNI', 'flag_DNI', 'DHI', 'flag_DHI']

    if sep1 and sep2:
        # Separate data based on provided separators
        df_3m = df.loc[:sep1]
        df_1m = df.loc[sep1:sep2]

        df_1m = df_1m.resample('3T').mean()

        df = pd.concat([df_3m, df_1m])
    else:
        df = df.resample('3T').mean()

    # Completion
    datarange_3m = pd.date_range('2005-01-01 00:00:00', '2023-11-08 23:59:00', freq='3T')
    df_3m_merged = pd.merge(df, pd.DataFrame(index=datarange_3m), right_index=True, left_index=True, how='outer')
    df_3m_co = df_3m_merged.fillna(value={'GHI': -9999.9, 'DNI': -9999.9, 'DHI': -9999.9, 'flag_GHI': 1, 'flag_DNI': 1, 'flag_DHI': 1})
    df_3m_co[['flag_GHI', 'flag_DNI', 'flag_DHI']] = df_3m_co[['flag_GHI', 'flag_DNI', 'flag_DHI']].astype(int)

    return df_3m_co


