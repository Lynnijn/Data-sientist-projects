import pandas as pd
import os
import numpy as np


def extract_from_metadata(file_name, metadata):
    site_name = os.path.splitext(file_name)[0]
    matching_stations = metadata[metadata['station name'].apply(lambda x: site_name.startswith(x))]

    if not matching_stations.empty:
        latitude = matching_stations['latitude'].values[0]
        longitude = matching_stations['longitude'].values[0]
        
    return site_name, latitude, longitude

        
        
def extract_from_final_data(df):        
    start_times = []
    end_times = []
    completenesses = []
    pyrnanometer_types = []
    parameter_ids = []
    device_types = []
    
    for variable in df.columns:
        start_time = pd.Timestamp(df[variable].first_valid_index())
        start_times.append(start_time)

        end_time = pd.Timestamp(df[variable].last_valid_index())
        end_times.append(end_time)

        completeness = "%.2f" % float((1 - df.loc[f'{start_time}':f'{end_time}', variable].isna().mean())*100)
        completenesses.append(completeness)

        variable_to_pyrnanometer_type = {
            'ghi': 'Precision Spectral Pyranometer (PSP)',
            'dni': 'Normal Incidence Pryheliometer (NIP)',
            'dhi': 'Eppley 8-48 "black and white" pyranometer',
        }
        pyrnanometer_type = variable_to_pyrnanometer_type.get(variable, np.nan)
        pyrnanometer_types.append(pyrnanometer_type)
        
        device_type = 'pyrheliometer' if (variable == 'dni') else 'pyranometer'
        device_types.append(device_type)
            
        parameter_id = variable if (variable in ['ghi', 'dni', 'dhi']) else np.nan
        parameter_ids.append(parameter_id)

    freq_str = pd.infer_freq(df.index)
    numeric_part = int(''.join(filter(str.isdigit, freq_str))) if any(c.isdigit() for c in freq_str) else 1
    frequency_part = ''.join(filter(str.isalpha, freq_str))
    timedelta_obj = pd.Timedelta(numeric_part, unit=frequency_part)
    
    return start_times, end_times, completenesses, device_types, pyrnanometer_types, parameter_ids, timedelta_obj
  



def extract_from_yaml_file(solrad_info, df):
    source = solrad_info.get('name', '')
    domain = solrad_info.get('domain', '')
    classification = solrad_info.get('classification', '')
    temporal_aggregation_method = solrad_info.get('temporal_aggregation_method', '')
    temporal_aggregation_convention = solrad_info.get('temporal_aggregation_convention', '')
    
    units = []
    for variable in df.columns:
        unit = solrad_info.get('unit', '') if (variable in ['ghi', 'dni', 'dhi']) else np.nan
        units.append(unit)
    
    
    return source, domain, classification, units, temporal_aggregation_method, temporal_aggregation_convention
