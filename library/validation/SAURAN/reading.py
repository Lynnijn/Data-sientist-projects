import os
import pandas as pd


def get_station_names(raw_path):
    station_names = []

    for station_folder in os.listdir(raw_path):
        station_path = os.path.join(raw_path, station_folder)

        if os.path.isdir(station_path):
            station_names.append(station_folder)

    return station_names


def read_data_for_station_csv(raw_path, station_name, skiprows=4, header=None):
    df_list = []

    folder_path = os.path.join(raw_path, station_name)
    
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)

        for file in files:
            if file.endswith(".csv"):
                data_file_path = os.path.join(folder_path, file)
                df_list.append(pd.read_csv(data_file_path, skiprows=skiprows, header=header))

    if not df_list:
        print(f"No data found for station: {station_name}")
        return None

    df_full = pd.concat(df_list, ignore_index=True)

    return df_full

