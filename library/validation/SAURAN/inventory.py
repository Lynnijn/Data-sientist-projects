import pandas as pd
import os
import numpy as np
import re

from eee.pandas_util import infer_index_freq


def extract_from_metadata(file_name, metadata):
    site_name = os.path.splitext(file_name)[0]
    matching_stations = metadata[metadata['station name'].apply(lambda x: site_name.startswith(x))]

    if not matching_stations.empty:
        latitude = matching_stations['latitude'].values[0]
        longitude = matching_stations['longitude'].values[0]
        
    return site_name, latitude, longitude

        
        
def extract_from_final_data(df, file_name):        
    start_times = []
    end_times = []
    completenesses = []
    parameter_ids = []
    
    for variable in df.columns:
        start_time = pd.Timestamp(df[variable].first_valid_index())
        start_times.append(start_time)

        end_time = pd.Timestamp(df[variable].last_valid_index())
        end_times.append(end_time)

        completeness = "%.2f" % float((1 - df.loc[f'{start_time}':f'{end_time}', variable].isna().mean())*100)
        completenesses.append(completeness)
            
        parameter_id = variable if (variable in ['ghi', 'dni', 'dhi']) else np.nan
        parameter_ids.append(parameter_id)

    if file_name == 'usaid_namibian_university_of_science_and_technology.csv':
        timedelta_obj = pd.Timedelta(1, 'Minutes')
    else:
        freq_str = str(infer_index_freq(pd.DatetimeIndex(df.index)))
        matches = re.findall(r'(?:(\d+)\s*\*\s*)?(\w+)', freq_str)
        numeric_part, frequency_part = matches[0] if matches[0] else (1, 'Minutes')
        numeric_value = int(numeric_part) if numeric_part and numeric_part.isdigit() else 1
        timedelta_obj = pd.Timedelta(numeric_value, unit=frequency_part)
    
    return start_times, end_times, completenesses, parameter_ids, timedelta_obj
  



def extract_from_yaml_file(solrad_info, df):
    device_types = []
    pyranometer_types = []
    
    source = solrad_info.get('name', '')
    domain = solrad_info.get('domain', '')
    units = solrad_info.get('unit', '')
    classification = solrad_info.get('classification', '')
    temporal_aggregation_method = solrad_info.get('temporal_aggregation_method', '')
    temporal_aggregation_convention = solrad_info.get('temporal_aggregation_convention', '')
    
    
    for variable in df.columns:
        device_type = 'pyrheliometer' if (variable == 'dni') else 'pyranometer'
        pyranometer_type = 'Kipp & Zonen CHP1' if (variable == 'dni') else 'Kipp & Zonen CMP11'

        device_types.append(device_type)
        pyranometer_types.append(pyranometer_type)

    
    
    return source, domain, classification, device_types, pyranometer_types, units, temporal_aggregation_method, temporal_aggregation_convention
