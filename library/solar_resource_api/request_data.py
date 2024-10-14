import copy
from dataclasses import dataclass
import json
import requests
import time


def add_legacy_authorization(
    params: dict,
    token: str,
) -> dict:
    
    params["authorization"] = token
    
    return params

@dataclass
class SolarTrackingSystem:
    track_max_angle: float
    track_backtrack: bool = None
    track_ground_coverage_ratio: float = None
    track_cross_shed_slope: float = None
    track_dual_axis: bool = None
    azimuth: float = None
    inclination: float = None

@dataclass
class HistoricalRequest:
    latitude: float
    longitude: float
    variables: list
    resolution: str
    start: str
    end: str
    azimuth: float = None
    inclination: float = None
    solar_tracking_system: SolarTrackingSystem = None
    
    def parse_params(self) -> dict:
        
        params = {}
        params["latitude"] = self.latitude
        params["longitude"] = self.longitude
        params["variables"] = self.variables
        params["resolution"] = self.resolution
        params["start"] = self.start
        params["end"] = self.end
        if self.azimuth:
            params["azimuth"] = self.azimuth
        if self.inclination:
            params["inclination"] = self.inclination
        if self.solar_tracking_system:
            params["track_max_angle"] = self.solar_tracking_system.track_max_angle
            if self.solar_tracking_system.track_backtrack:
                params["track_backtrack"] = self.solar_tracking_system.track_backtrack
            if self.solar_tracking_system.track_ground_coverage_ratio:
                params["track_ground_coverage_ratio"] = self.solar_tracking_system.track_ground_coverage_ratio            
            if self.solar_tracking_system.track_cross_shed_slope:
                params["track_cross_shed_slope"] = self.solar_tracking_system.track_cross_shed_slope
            if self.solar_tracking_system.track_dual_axis:
                params["track_dual_axis"] = self.solar_tracking_system.track_dual_axis
            if self.solar_tracking_system.azimuth:
                params["azimuth"] = self.solar_tracking_system.azimuth
            if self.solar_tracking_system.inclination:
                params["inclination"] = self.solar_tracking_system.inclination  
        
        return params
                
    def legacy_post_and_get_results(
        self,
        token: str,
        url: str,
    ):
        
        start_time = time.time()
        params = self.parse_params()
        params["variables"] = ",".join(params["variables"])
        params = add_legacy_authorization(params=params, token=token)
        request_results = requests.get(url=url, params=params)
        if request_results.status_code!= 200:
            print("Could not retrieve the results"
                  f"/nStatus: {request_results.status_code}")
        request_results_json =  json.loads(request_results.text)
        execution_time = round(time.time() - start_time, 1)

        return request_results_json, execution_time
    

@dataclass
class TMYRequest:
    latitude: float
    longitude: float
    variables: list
    resolution: str
    azimuth: float = None
    inclination: float = None
    solar_tracking_system: SolarTrackingSystem = None
    
    def parse_params(self) -> dict:
        
        params = {}
        params["latitude"] = self.latitude
        params["longitude"] = self.longitude
        params["variables"] = self.variables
        params["resolution"] = self.resolution
        if self.azimuth:
            params["azimuth"] = self.azimuth
        if self.inclination:
            params["inclination"] = self.inclination
        if self.solar_tracking_system:
            params["track_max_angle"] = self.solar_tracking_system.track_max_angle
            if self.solar_tracking_system.track_backtrack:
                params["track_backtrack"] = self.solar_tracking_system.track_backtrack
            if self.solar_tracking_system.track_ground_coverage_ratio:
                params["track_ground_coverage_ratio"] = self.solar_tracking_system.track_ground_coverage_ratio            
            if self.solar_tracking_system.track_cross_shed_slope:
                params["track_cross_shed_slope"] = self.solar_tracking_system.track_cross_shed_slope
            if self.solar_tracking_system.track_dual_axis:
                params["track_dual_axis"] = self.solar_tracking_system.track_dual_axis
            if self.solar_tracking_system.azimuth:
                params["azimuth"] = self.solar_tracking_system.azimuth
            if self.solar_tracking_system.inclination:
                params["inclination"] = self.solar_tracking_system.inclination  
        
        return params
                
    def legacy_post_and_get_results(
        self,
        token: str,
        url: str,
    ):
        
        start_time = time.time()
        params = self.parse_params()
        params["variables"] = ",".join(params["variables"])
        params = add_legacy_authorization(params=params, token=token)
        request_results = requests.get(url=url, params=params)
        if request_results.status_code!= 200:
            print("Could not retrieve the results"
                  f"/nStatus: {request_results.status_code}")
        request_results_json =  json.loads(request_results.text)
        execution_time = round(time.time() - start_time, 1)

        return request_results_json, execution_time
