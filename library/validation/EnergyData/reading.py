import os
import pandas as pd
import re


def read_metadata_for_station(info_path):
    metadata = []
    
    files = os.listdir(info_path)
    for file in files:
        data_file_path = os.path.join(info_path, file)

        if file.endswith(".csv"):
            print(f'reading {file}')
        
            with open(data_file_path, 'r', errors = 'ignore') as file:
                df_info = pd.read_csv(file, sep=';')

            station_name = df_info.iloc[0,1].lstrip()
            latitude = "%.3f" % float(df_info.iloc[4,1])
            longitude = "%.3f" % float(df_info.iloc[5,1])
            elevation = df_info.iloc[3,1]
            time = int(re.search(r'\b(\d+)\b', df_info.iloc[10,1]).group(1))
            tz = df_info.iloc[8,1]

            metarow = {'station name': station_name, 'latitude': latitude, 'longitude': longitude, 'elevation (m)': elevation, 'time resolution': time, 'time zone': tz}
 

        elif file.endswith("header.xlsx"):
            print(f'reading {file}')
            
            df_info = pd.read_excel(data_file_path)

            station_name = df_info.iloc[0,1].lstrip()
            latitude = "%.3f" % float(df_info.iloc[4,1])
            longitude = "%.3f" % float(df_info.iloc[5,1])
            elevation = df_info.iloc[3,1]
            time = int(re.search(r'\b(\d+)\b', df_info.iloc[10,1]).group(1))
            tz = df_info.iloc[8,1]

            metarow = {'station name': station_name, 'latitude': latitude, 'longitude': longitude, 'elevation (m)': elevation, 'time resolution': time, 'time zone': tz}

            
        elif file.endswith("header_fr_en.xlsx"):
            print(f'reading {file}')
            
            df_info = pd.read_excel(data_file_path)

            station_name = df_info.iloc[5,1].split('/')[1].lstrip()
            latitude = "%.3f" % float(re.search(r'([\d.]+)', df_info.iloc[6,1].split(',')[0]).group(1))
            longitude = "%.3f" % float(re.search(r'([\d.]+)', df_info.iloc[6,1].split(',')[1]).group(1))
            elevation = int(re.search(r'\b(\d+)\b', df_info.iloc[6,1].split(',')[2]).group(1))
            time = str(df_info.iloc[13,1])[0]
            tz = df_info.iloc[12,1]
        
            metarow = {'station name': station_name, 'latitude': latitude, 'longitude': longitude, 'elevation (m)': elevation, 'time resolution': time, 'time zone': tz}
        
        
        else:
            print(f'reading {file}')
        
            df_info = pd.read_excel(data_file_path)
        
            station_name = df_info.iloc[2,0].split(':')[1].lstrip()
            latitude = "%.3f" % float(df_info.iloc[3,0].split(':')[1])
            longitude = "%.3f" % float(df_info.iloc[4,0].split(':')[1])
            elevation = int(df_info.iloc[5,0].split(':')[1])
            time = int(re.search(r'(\d+)', df_info.iloc[8,0]).group(1))
            tz = int(df_info.iloc[7,0].split(':')[1])
 
            metarow = {'station name': station_name, 'latitude': latitude, 'longitude': longitude, 'elevation (m)': elevation, 'time resolution': time, 'time zone': tz}
    

        metadata.append(metarow)
        
    return metadata
         
            
            
            
            
            
            
            
            