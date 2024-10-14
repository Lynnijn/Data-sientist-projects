import pandas as pd
import os
import numpy as np
import re
from eee.pandas_util import infer_index_freq
import library.validation.parsing as parsing


def extract_from_metadata(site_name, metadata):
    matching_stations = metadata.loc[metadata['normalized station name'] == site_name]
    latitude, longitude = None, None
    
    if not matching_stations.empty:    
        latitude = metadata.loc[matching_stations.index[0],'latitude']
        longitude = metadata.loc[matching_stations.index[0],'longitude']
        
    return latitude, longitude

        
        
def extract_from_final_data(df):        
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

        parameter_id = variable.split('_')[-1] if not ('qflag' in variable) else np.nan
        parameter_ids.append(parameter_id)



    freq_str = str(infer_index_freq(pd.DatetimeIndex(df.index)))
    matches = re.findall(r'(?:(\d+)\s*\*\s*)?(\w+)', freq_str)
    numeric_part, frequency_part = matches[0] if matches[0] else (1, 'Minutes')
    numeric_value = int(numeric_part) if numeric_part and numeric_part.isdigit() else 1
    timedelta_obj = pd.Timedelta(numeric_value, unit=frequency_part)
 
        
    return start_times, end_times, completenesses, parameter_ids, timedelta_obj
  



def extract_from_yaml_file(solrad_info, df):
    units = []
    
    source = solrad_info.get('name', '')
    domain = solrad_info.get('domain', '')
    classification = solrad_info.get('classification', '')
    temporal_aggregation_method = solrad_info.get('temporal_aggregation_method', '')
    temporal_aggregation_convention = solrad_info.get('temporal_aggregation_convention', '')
    for variable in df.columns:
        unit = solrad_info.get('unit', '') if not ('qflag' in variable) else np.nan
        units.append(unit)
   
    
    return source, domain, classification, units, temporal_aggregation_method, temporal_aggregation_convention




def get_device(site_name, variable):    
    device_type = 'pyranometer'
    
    if 'qflag' in variable:
        device_type = None
       


    elif site_name in ['hrazdan', 'masrik', 'talin', 'yerevanagro']:
        if '2_dni' in variable:
            device_type = 'sun photometer'
            
    elif site_name in 'bdfe2_feni' or 'vn' in site_name or 'benin' in site_name or 'burkina' in site_name or 'côte_d_ivoire' in site_name or 'gambia' in site_name or 'ghana' in site_name or 'liberia' in site_name or 'nigeria' in site_name or 'senegal' in site_name or 'sierra' in site_name or 'np' in site_name or 'pk' in site_name or site_name in ['tarambaly_guinea', 'edg_substation_kankan_guinea', 'mw_solar_chileka_dccms']:
        if 'dni' in variable:
            device_type = 'pyrheliometer'
            
    elif 'guinea_bissau' in site_name or 'mali' in site_name or 'togo' in site_name or 'pk' in site_name or site_name in 'nigelec_substation_lossa_niger':
        if '2_ghi' in variable:
            device_type = 'rotating_shadowband_irradiometer'       

    elif 'lb' in site_name:
        if 'dni' in variable or '2_ghi' in variable:
            device_type = 'rotating_shadowband_irradiometer'

    elif 'mw' in site_name or 'mv' in site_name or site_name in ['zm_solar_mutanda_zari', 'zm_solar_kasama_zari', 'zm_solar_kaoma_zari', 'zm_solar_choma_zari', 'zm_solar_chilanga_zari']:
        if 'dni' in variable or '2_ghi' in variable or 'dhi' in variable:
            device_type = 'rotating_shadowband_irradiometer'
            
    elif site_name in ['solar_shinyanga_world_bank', 'solar_dodoma_world_bank', 'solar_dar_es_salaam_world_bank']:
        if '1_dni' in variable:
            device_type = 'pyrheliometer'
        if '2_dni' in variable:
            device_type = 'derived_from_other_irre_components'

    elif 'sn' in site_name:
        if 'dhi' in variable:
            device_type = 'rotating_shadowband_irradiometer'
        
    return device_type

                                 
                                 
                                 
def get_pyranometer(site_name, variable):
    pyranometer_type = None
 
    if 'benin' in site_name or 'burkina' in site_name or 'côte_d_ivoire' in site_name or 'gambia' in site_name or 'ghana' in site_name or 'liberia' in site_name or 'nigeria' in site_name or 'senegal' in site_name or 'sierra' in site_name:
        if any(v in variable for v in ['ghi', 'dhi']):
            pyranometer_type = 'CMP10'
            
        elif 'dni' in variable:
            pyranometer_type = 'CHP1'
            
    elif site_name == ['solar_narok_world_bank', 'solar_laisamis_world_bank', 'solar_homa_bay_world_bank']:
        if 'dhi' in variable:
            pyranometer_type = 'Delta-T SPN1'
        
        elif '1_ghi' in variable:
            pyranometer_type = 'Hukseflux SR20-T2'
            
        elif '2_ghi' in variable:
            pyranometer_type = 'Kipp & Zonen CMP10'
            
    elif 'np' in site_name:
        if '2_dhi' in variable:
            pyranometer_type = 'Hukseflux SR20-T2'
            
    elif site_name in ['solar_shinyanga_world_bank', 'solar_dodoma_world_bank', 'solar_dar_es_salaam_world_bank']:
        if '1_dni' in variable:
            pyranometer_type = 'Hukseflux DR20'
            
        elif 'ghi' in variable:
            pyranometer_type = 'Hukseflux SR20-T2'
    
    elif site_name in ['solar_wadelai_world_bank', 'solar_soroti_world_bank']:
        if '1_ghi' in variable:
            pyranometer_type = 'Kipp & Zonen CMP10 163400'
            
        elif '2_ghi' in variable:
            pyranometer_type = 'Kipp & Zonen CMP10 163401'
            
        elif 'dhi' in variable:
            pyranometer_type = 'Delta-T SPN1'
            
    elif 'sn' in site_name:
        if '1_ghi' in variable:
            pyranometer_type = 'silicon pyranometer'

        
        
    return pyranometer_type
            

    
def extract_device(site_name, df):
    device_types = []
    pyrnanometer_types = []
    
    for variable in df.columns:
        device_type = get_device(site_name, variable)
        device_types.append(device_type)
            
        pyrnanometer_type = get_pyranometor(site_name, variable)
        pyrnanometer_types.append(pyrnanometer_type)
        
    return device_types, pyrnanometer_types