import os
import pandas as pd
import datetime


def get_station_names(raw_path):
    station_names = []

    for station_file in os.listdir(raw_path):
        if station_file.endswith(".csv"):
            station_names.append(station_file)

    return station_names


def read_data_for_station_csv(station_name):
    
    ticket_path_flu = "/home/lhn3e/OneDrive-3E/Research/Solar/tickets/2023/IN2818_FLUXNET_measurement_data"
    data_file_path =  os.path.join(ticket_path_flu, 'raw_data', f'{station_name}.csv')

    df = pd.read_csv(data_file_path)

    return df


def parse_flu(df):
    df_full = df.copy()
    
    # Index 1
    df_full.index = pd.to_datetime(df_full['TIMESTAMP_START'], format = '%Y%m%d%H%M')
    
    # Keep columns
    cols_to_keep = ['TIMESTAMP_END','SW_IN']
    df_full = df_full.loc[:, cols_to_keep]
    
    # Datetime 2
    df_full['TIMESTAMP_END'] = pd.to_datetime(df_full['TIMESTAMP_END'], format = '%Y%m%d%H%M')

    # Rename 3
    df_full = df_full.rename(columns={'SW_IN': 'GHI'})
        
    return df_full