import pandas as pd
import requests
from geopy.geocoders import Nominatim

URLS = {
    "Africa": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Africa",
    "Asia": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Asia",
    "Europe": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Europe",
    "North America": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_North_America",
    "Ocenia": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_Oceania",
    "South America": "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_in_South_America",
}



def get_continents_and_countries() -> dict[str, str]:
    """Helper function to get countries and corresponding continents.

    Returns:
        Dictionary where keys are countries and values are continents.

    """
    df_ = pd.concat(
        [
            pd.DataFrame(
                pd.read_html(
                    requests.get(url).text.replace("<br />", ";"),
                    match="Flag",
                )[0]
                .pipe(
                    lambda df_: df_.rename(
                        columns={col: i for i, col in enumerate(df_.columns)}
                    )
                )[2]
                .astype(str)
                .str.split(";;")
                .apply(lambda x: x[0])
            )
            .assign(continent=continent)
            .rename(columns={2: "country"})
            for continent, url in URLS.items()
        ]
    ).reset_index(drop=True)
    df_["country"] = (
        df_["country"]
        .str.replace("*", "", regex=False)
        .str.split("[")
        .apply(lambda x: x[0])
    ).str.replace("\xa0", "")
    return dict(df_.to_dict(orient="split")["data"])



def get_location_of(coo: str, data: dict[str, str]) -> tuple[str, str, str]:
    """Function to get the country of given coordinates.

    Args:
        coo: coordinates as string ("lat, lon").
        data: input dictionary of countries and continents.

    Returns:
        Tuple of coordinates, country and continent (or Unknown if country not found).

    """
    geolocator = Nominatim(user_agent="stackoverflow", timeout=25)
    country: str = (
        geolocator.reverse(coo, language="en-US").raw["display_name"].split(", ")[-1]
    )
    return (coo, country, data.get(country, "Unknown"))

continents_and_countries = get_continents_and_countries()






# def get_continents_and_countries() -> dict[str, str]:
#     df_ = pd.concat(
#         [
#             pd.DataFrame(
#                 pd.read_html(
#                     requests.get(url).text.replace("<br />", ";"),
#                     match="Flag",
#                 )[0]
#                 .pipe(
#                     lambda df_: df_.rename(
#                         columns={col: i for i, col in enumerate(df_.columns)}
#                     )
#                 )[2]
#                 .astype(str)
#                 .str.split(";;")
#                 .apply(lambda x: x[0])
#             )
#             .assign(continent=continent)
#             .rename(columns={2: "country"})
#             for continent, url in URLS.items()
#         ]
#     ).reset_index(drop=True)
#     df_["country"] = (
#         df_["country"]
#         .str.replace("*", "", regex=False)
#         .str.split("[")
#         .apply(lambda x: x[0])
#     ).str.replace("\xa0", "")
#     return dict(df_.to_dict(orient="split")["data"])


# def get_location_info(lat_lon):
#     geolocator = Nominatim(user_agent="stackoverflow", timeout=25)
#     location = geolocator.reverse(lat_lon, language='en')
#     country = location.raw['address']['country']
#     continent = continents_and_countries.get(country, None) 

#     return country, continent


# continents_and_countries = get_continents_and_countries()
