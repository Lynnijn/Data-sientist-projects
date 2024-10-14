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

        
        
# def extract_from_final_data(df):        
#     start_times = []
#     end_times = []
#     completenesses = []
#     parameter_ids = []
    
#     for variable in df.columns:
#         start_time = pd.Timestamp(df[variable].first_valid_index())
#         start_times.append(start_time)

#         end_time = pd.Timestamp(df[variable].last_valid_index())
#         end_times.append(end_time)

#         completeness = "%.2f" % float((1 - df.loc[f'{start_time}':f'{end_time}', variable].isna().mean())*100)
#         completenesses.append(completeness)

#         parameter_id = variable.split('_')[-1]
#         parameter_ids.append(parameter_id)

#     freq_str = str(infer_index_freq(pd.DatetimeIndex(df.index)))
#     matches = re.findall(r'(?:(\d+)\s*\*\s*)?(\w+)', freq_str)
#     numeric_part, frequency_part = matches[0] if matches[0] else (1, 'Minutes')
#     numeric_value = int(numeric_part) if numeric_part and numeric_part.isdigit() else 1
#     timedelta_obj = pd.Timedelta(numeric_value, unit=frequency_part)
 
        
#     return start_times, end_times, completenesses, parameter_ids, timedelta_obj
  
def extract_from_final_data(df):        
    start_times = []
    end_times = []
    completenesses = []
    parameter_ids = []
    
    # Ensure the index of df is in datetime format
    df.index = pd.to_datetime(df.index)
    
    for variable in df.columns:
        start_time = df[variable].first_valid_index()
        end_time = df[variable].last_valid_index()
        if isinstance(start_time, pd.Timestamp) and isinstance(end_time, pd.Timestamp):
            start_time = start_time.to_pydatetime()
            end_time = end_time.to_pydatetime()
            start_times.append(start_time)
            end_times.append(end_time)
            completeness = "%.2f" % float((1 - df.loc[start_time:end_time, variable].isna().mean()) * 100)
            completenesses.append(completeness)
            parameter_id = variable.split('_')[-1]
            parameter_ids.append(parameter_id)

    freq_str = str(infer_index_freq(pd.DatetimeIndex(df.index)))
    matches = re.findall(r'(?:(\d+)\s*\*\s*)?(\w+)', freq_str)
    numeric_part, frequency_part = matches[0] if matches[0] else (1, 'Minutes')
    numeric_value = int(numeric_part) if numeric_part and numeric_part.isdigit() else 1
    timedelta_obj = pd.Timedelta(numeric_value, unit=frequency_part)
        
    return start_times, end_times, completenesses, parameter_ids, timedelta_obj



def extract_from_yaml_file(solrad_info, df):
    source = solrad_info.get('name', '')
    domain = solrad_info.get('domain', '')
    classification = solrad_info.get('classification', '')
    temporal_aggregation_method = solrad_info.get('temporal_aggregation_method', '')
    temporal_aggregation_convention = solrad_info.get('temporal_aggregation_convention', '')
    units = solrad_info.get('unit', '')
   
    
    return source, domain, classification, units, temporal_aggregation_method, temporal_aggregation_convention




def get_device(site_name, variable):    
    device_type = 'pyranometer'
       

    if site_name in ['cal_poly_humboldt_sorms', 'nrel_solar_radiation_research_laboratory_irradiance_inc_rsp_v2', 'solrmap_kalaeloa_oahu_rsr', 'lowry_range_solar_station_rsr', 'solrmap_la_ola_lanai_rsr', 'sacramento_municipal_utility_district_anatolia', 'solrmap_southwest_solar_research_park', 'sun_spot_one_san_luis_valley_rsr', 'solrmap_sun_spot_two_swink_rsr', 'solrmap_utah_geological_survey_state_energy_program_cedar_city', 'solrmap_utah_geological_survey_state_energy_program_milford', 'solrmap_loyola_marymount_university_rsr', 'nrel_solar_radiation_research_laboratory_ati_rsp', 'nrel_solar_radiation_research_laboratory_yes_mfr', 'nrel_solar_radiation_research_laboratory_schott_rsp', 'oak_ridge_national_laboratory_rsr']:
        if 'dni' in variable:
            device_type = 'derived_from_other_irre_components'
            
    elif site_name in 'nrel_solar_radiation_research_laboratory_razon':
        if 'ghi' in variable:
            device_type = 'derived_from_other_irre_components'
            
    elif site_name in ['university_of_nevada_las_vegas', 'nrel_solar_radiation_research_laboratory_aocs', 'nevada_power_clark_station']:
        if 'dhi' in variable:
            device_type = 'derived_from_other_irre_components'       

    elif site_name in ['elizabeth_city_state_university', 'nrel_solar_radiation_research_laboratory_razon', 'nevada_power_clark_station']:
        if 'dni' in variable:
            device_type = 'pyrheliometer'

    else:
        device_type = 'pyranometer'
                    
        
    return device_type

                                 
                                 
                                 
def get_pyranometer(site_name, variable):
    pyranometer_type = None
 
    if site_name == 'Cal Poly Humboldt (SoRMS)':
        if any(v in variable for v in ['ghi', 'dni']):
            pyranometer_type = None
            
        elif 'dhi' in variable:
            pyranometer_type = 'PSP'
            
    elif site_name == 'NREL Energy Systems Integration Facility':
        pyranometer_type = 'Silicon Pyranometer'
        
    elif site_name in ['nrel_solar_radiation_research_laboratory_irradiance_inc_rsp_v2', 'solrmap_kalaeloa_oahu_rsr', 'lowry_range_solar_station_rsr', 'solrmap_la_ola_lanai_rsr', 'sacramento_municipal_utility_district_anatolia', 'solrmap_southwest_solar_research_park', 'sun_spot_one_san_luis_valley_rsr', 'solrmap_sun_spot_two_swink_rsr', 'solrmap_utah_geological_survey_state_energy_program_cedar_city', 'solrmap_utah_geological_survey_state_energy_program_milford', 'solrmap_loyola_marymount_university_rsr', 'south_park_mountain_data', 'nrel_solar_radiation_research_laboratory_ati_rsp', 'nrel_solar_radiation_research_laboratory_schott_rsp', 'us_virgin_islands_bovoni_2', 'us_virgin_islands_longford', 'oak_ridge_national_laboratory_rsr']:
        if any(v in variable for v in ['ghi', 'dhi']):
            pyranometer_type = 'LICOR LI-200 Pyranometer'
            
    elif site_name == 'nrel_solar_radiation_research_laboratory_aocs':
        if 'dni' in variable:
            pyranometer_type = 'LICOR LI-200 Pyranometer'

    elif site_name == 'nrel_solar_radiation_research_laboratory_razon':
        if 'dni' in variable:
            pyranometer_type = 'Kipp & Zonen PH1 smart thermopile pyrheliometer'
                                 
        if 'dhi' in variable:
            pyranometer_type = 'Kipp & Zonen PH1 smart thermopile pyranometer'
                                 
    elif site_name == 'solar_technology_acceleration_center_solartac':
        if 'dhi' in variable:
            pyranometer_type = 'Black & White Pyranometer'
            
    elif site_name == 'bluefield_state_college':
        pyranometer_type = 'Eppley Laboratory, Inc. Model PSP '
        
    elif site_name == 'elizabeth_city_state_university':
        if 'ghi' in variable:
            pyranometer_type = 'Eppley Laboratory, Inc. Model PSP'
            
        elif 'dni' in variable:
            pyranometer_type = 'Eppley Laboratory, Inc. Model NIP (Normal Incidence Pyrheliometer)'
            
        elif 'dni' in variable:
            pyranometer_type = 'PSP'
            
    elif site_name == 'nrel_solar_radiation_research_laboratory_yes_mfr':
        if any(v in variable for v in ['ghi', 'dhi']):
            pyranometer_type = 'thermopile pyranometer'
            
    elif site_name == 'nevada_power_clark_station':
        if 'ghi' in variable:
            pyranometer_type = 'Kipp & Zonen Model CMP3 Pyranometer'
            
        if 'dni' in variable:
            pyranometer_type = 'Eppley Laboratory, Inc. Model NIP'    
            
    else:
        pyranometer_type = None
            
        
        
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