from dataclasses import dataclass
import requests
import pandas as pd
import os
from pathlib import Path

from shapely.geometry import Point
from geopy.distance import geodesic
import geopandas as gpd

import fiona
import shapely.geometry

import rasterio


from eee.solar.model import Location
from library.solar_resource_api.request_data import HistoricalRequest


coastline_file = Path.home()/"OneDrive-3E/Research/Solar/tickets/2023/IN3046_factors/coastline/ne_10m_coastline.shp"

terrain_file = Path.home()/"OneDrive-3E/Research/Solar/tickets/2024/IN3043_accuracy_factors_analysis/terrain_complexity/dragut_eisank_2012/Level3.shp"

tpi_1KMmd_SRTM_file = Path.home()/"OneDrive-3E/Research/Solar/tickets/2024/IN3043_accuracy_factors_analysis/terrain_complexity/amatulli_2018/tpi_1KMmd_SRTM.tif"
tpi_5KMmd_SRTM_file = Path.home()/"OneDrive-3E/Research/Solar/tickets/2024/IN3043_accuracy_factors_analysis/terrain_complexity/amatulli_2018/tpi_5KMmd_SRTM.tif"
tpi_10KMmd_SRTM_file = Path.home()/"OneDrive-3E/Research/Solar/tickets/2024/IN3043_accuracy_factors_analysis/terrain_complexity/amatulli_2018/tpi_10KMmd_SRTM.tif"
tri_1KMmd_SRTM_file = Path.home()/"OneDrive-3E/Research/Solar/tickets/2024/IN3043_accuracy_factors_analysis/terrain_complexity/amatulli_2018/tri_1KMmd_SRTM.tif"
tri_5KMmd_SRTM_file = Path.home()/"OneDrive-3E/Research/Solar/tickets/2024/IN3043_accuracy_factors_analysis/terrain_complexity/amatulli_2018/tri_5KMmd_SRTM.tif"
tri_10KMmd_SRTM_file = Path.home()/"OneDrive-3E/Research/Solar/tickets/2024/IN3043_accuracy_factors_analysis/terrain_complexity/amatulli_2018/tri_10KMmd_SRTM.tif"

SOLAR_RESOURCE_KEY = os.environ["EEE_SOLAR_API_LEGACY_KEY"]
solar_resource_url = "https://api.3elabs.eu/solardata?"

times = pd.date_range(start="2022-01-01", end="2024-01-01", freq="H")


@dataclass
class ComplexityFactor:
    standard_name: str
    value: [str, float]

    def _validate_if_standard_name_in_registry(self):
        if self.standard_name not in self.value[0]:
            raise ValueError("Invalid standard name")

@dataclass
class SiteComplexity:
    name: str
    latitude: float
    longitude: float
    altitude: float
    clouds_persistence: ComplexityFactor = None
    _climate: ComplexityFactor = None
    _distance_to_coastline_km: float = None 
    _terrain_classification: ComplexityFactor = None
    _clearness: float = None

    @property
    def climate(self):
        return self._climate

    def fetch_climate_info(self):
        api_url = "http://climateapi.scottpinkelman.com/api/v1/location/{lat}/{lon}"
        response = requests.get(api_url.format(lat=self.latitude, lon=self.longitude))

        if response.status_code == 200:
            result = response.json()

            if 'return_values' in result:
                climate_zone = result["return_values"][0].get("koppen_geiger_zone", "Climate zone not available")
                zone_description = result["return_values"][0].get("zone_description", "Description not available")

                self._climate = ComplexityFactor(standard_name="climate_zone", value=climate_zone)
                self.zone_description = ComplexityFactor(standard_name="zone_description", value=zone_description)
            else:
                print(f"No climate data available for {self.latitude}, {self.longitude}")
        else:
            print(f"Failed to retrieve climate data for {self.latitude}, {self.longitude}")

    @property
    def distance_to_coastline_km(self):
        return self._distance_to_coastline_km

    def calculate_distance_to_coastline(self):
        coastline_data = gpd.read_file(coastline_file).to_crs(crs="EPSG:4326")

        site_point = Point(self.longitude, self.latitude)
        closest_line = coastline_data.geometry.distance(site_point).idxmin()
        closest_line_geometry = coastline_data.geometry.iloc[closest_line]
        closest_point_on_line = closest_line_geometry.interpolate(closest_line_geometry.project(site_point))
        self._distance_to_coastline_km = geodesic((self.latitude, self.longitude),
                                                  (closest_point_on_line.y, closest_point_on_line.x)).kilometers

        
        
    @property
    def terrain_classification(self):
        return self._terrain_classification

    def fetch_terrain_classification(self):
        with fiona.open(terrain_file) as fiona_collection:
            for shapefile_record in fiona_collection:
                shape = shapely.geometry.shape(shapefile_record['geometry'])

                point = shapely.geometry.Point(self.longitude, self.latitude)

                if shape.contains(point):
                    self._terrain_classification = ComplexityFactor(
                        standard_name="terrain_classification",
                        value=shapefile_record['properties']['Class_name']
                    )
                    break 

    @property
    def tri_1km(self):
        return self._tri_1km
    
    def fetch_tri_1km_value(self):
        with rasterio.open(tri_1KMmd_SRTM_file) as src:
            row, col = src.index(self.longitude, self.latitude)
            self._tri_1km = src.read(1)[row, col]

            
    @property
    def tri_5km(self):
        return self._tri_5km

    def fetch_tri_5km_value(self):
        with rasterio.open(tri_5KMmd_SRTM_file) as src:
            row, col = src.index(self.longitude, self.latitude)
            self._tri_5km = src.read(1)[row, col]
            
            
    @property
    def tri_10km(self):
        return self._tri_10km
    
    def fetch_tri_10km_value(self):
        with rasterio.open(tri_10KMmd_SRTM_file) as src:
            row, col = src.index(self.longitude, self.latitude)
            self._tri_10km = src.read(1)[row, col]


    @property
    def tpi_1km(self):
        return self._tpi_1km
    
    def fetch_tpi_1km_value(self):
        with rasterio.open(tpi_1KMmd_SRTM_file) as src:
            row, col = src.index(self.longitude, self.latitude)
            self._tpi_1km = src.read(1)[row, col]

            
    @property
    def tpi_5km(self):
        return self._tpi_5km

    def fetch_tpi_5km_value(self):
        with rasterio.open(tpi_5KMmd_SRTM_file) as src:
            row, col = src.index(self.longitude, self.latitude)
            self._tpi_5km = src.read(1)[row, col]
            
            
    @property
    def tpi_10km(self):
        return self._tpi_10km
    
    def fetch_tpi_10km_value(self):
        with rasterio.open(tpi_10KMmd_SRTM_file) as src:
            row, col = src.index(self.longitude, self.latitude)
            self._tpi_10km = src.read(1)[row, col]

            
            
    @property
    def clearness(self):
        return self._clearness
    
    def fetch_api_data(self):
        try:
            historical_request = HistoricalRequest(
                latitude=self.latitude,
                longitude=self.longitude,
                variables=["global_horizontal"],
                resolution="h",
                start="2022-01-01",
                end="2024-01-01"
            )

            prod_results_json, execution_time = historical_request.legacy_post_and_get_results(
                token=SOLAR_RESOURCE_KEY,
                url=solar_resource_url
            )

            # Convert API data to DataFrame
            api_data = pd.DataFrame(prod_results_json["data"], index=pd.DatetimeIndex(prod_results_json["index"]), columns=prod_results_json["columns"])
            self.api_sum = api_data.sum()
        except Exception as e:
            print(f"Error retrieving API data for site {self.name}: {str(e)}")
            self.api_sum = None

    def fetch_clearsky_data(self):
        try:
            location = Location(latitude=self.latitude, longitude=self.longitude, altitude=self.altitude)
            clearsky = location.get_irre_clearsky(times=times)

            # Ensure clearsky data has datetime index
            clearsky_data = clearsky["ghi"]
            clearsky_data.index = times

            # Sum clearsky data
            self.clearsky_sum = clearsky_data.sum()
        except Exception as e:
            print(f"Error retrieving Clearsky data for site {self.name}: {str(e)}")
            self.clearsky_sum = None

    def calculate_clearness(self):
        if self.api_sum is not None and self.clearsky_sum is not None and self.clearsky_sum != 0:
            self._clearness = (self.api_sum / self.clearsky_sum) * 100
        else:
            self._clearness = None
