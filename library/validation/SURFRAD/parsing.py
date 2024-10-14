import pandas as pd
import datetime



def parse(df):
    # Timestamp
    DateTime = df[[0, 2, 3, 4, 5]].apply(lambda s: datetime.datetime(*s), axis=1)
    df.index = DateTime

    # Keep columns
    cols_to_keep = [8, 9, 12, 13, 14, 15]
    df = df.iloc[:, cols_to_keep]

    # Rename columns
    df.columns = ['GHI', 'flag_GHI', 'DNI', 'flag_DNI', 'DHI', 'flag_DHI']

    # Separate data
    df_3m = df.loc['2005-01-01 00:00:00':'2008-12-31 23:57:00']
    df_1m = df.loc['2009-01-01 00:00:00':'2023-11-08 23:59:00']

    df_1m = df_1m.resample('3T').mean()

    df = pd.concat([df_3m, df_1m])

    # Complete records
    datarange_3m = pd.date_range('2005-01-01 00:00:00', '2023-11-08 23:59:00', freq='3T')
    df_3m_merged = pd.merge(df, pd.DataFrame(index=datarange_3m), right_index=True, left_index=True, how='outer')
    df_3m_co = df_3m_merged.fillna(value={'GHI': -9999.9, 'DNI': -9999.9, 'DHI': -9999.9, 'flag_GHI': 1, 'flag_DNI': 1, 'flag_DHI': 1})
    df_3m_co[['flag_GHI', 'flag_DNI', 'flag_DHI']] = df_3m_co[['flag_GHI', 'flag_DNI', 'flag_DHI']].astype(int)

    return df_3m_co


