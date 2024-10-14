import os

import pandas as pd
import geopandas as gpd
import ipyleaflet as ipl
import ipywidgets as ipw


# convert site to marker with popup
def _convert_site_to_marker_with_popup(
    gdf:gpd.GeoDataFrame,
    station:str,
    ):

    
    site_meta_html = ipw.HTML("""<b>station:</b> {station}<br>   
        <b>latitude:</b> {latitude}<br>
        <b>longitude:</b> {longitude}<br>
        <b>elevation:</b> {elevation}<br>
        <b>country:</b> {country}<br>
        <b>continent:</b> {continent}<br>
        <b>provider:</b> {provider}<br>""".format(station=station, 
                                                  latitude=round(gdf.loc[station]['latitude'], 2),
                                                  longitude=round(gdf.loc[station]['longitude'], 2),
                                                  elevation=round(gdf.loc[station]['elevation (m)'], 0),
                                                  country=gdf.loc[station]['country'],
                                                  continent=gdf.loc[station]['continent'],
                                                  provider=gdf.loc[station]['provider'],
                                                )
                             )

    site_marker = ipl.Marker(location=(gdf.loc[station]['latitude'], gdf.loc[station]['longitude']),
                    draggable=False)


    site_marker.popup = site_meta_html

    
    return site_marker


# instantiate map
class CustomMarker(ipl.Marker):
    def __init__(self, location, draggable=False, station=None, **kwargs):
        super().__init__(location=location, draggable=draggable, **kwargs)
        self.station = station
        
class IPLBaseMap(ipl.Map):
    def __init__(self,**kwargs):
        kwargs["zoom"] = kwargs.get("zoom", 2)
        
        kwargs["scroll_wheel_zoom"] = kwargs.get("scroll_wheel_zoom", True)
        
        super().__init__(**kwargs)
        
        self.add_control(ipl.LayersControl(position='topright'))

        self.add_control(ipl.FullScreenControl())

        search = ipl.SearchControl(position='topleft', 
                               url='https://nominatim.openstreetmap.org/search?format=json&q={s}',
                               zoom=5,
                               property_name='display_name')
    
        self.add_control(search)
        
        
# get map
def get_ipl_map(self):
    from library.map import IPLBaseMap

    map = IPLBaseMap()

    cluster = ipl.MarkerCluster(markers=self.markers, zoom=3, name='validation sites')

    map.add_layer(cluster)

    return map


