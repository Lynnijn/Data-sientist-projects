import numpy as np
import pandas as pd
import string
import re


def normalize_station_name(
    station_name: str,
) -> str:
    """
    Normalizes a station name.
    
    Parameters
    ----------
    station_name: str
        The station name to normalize
        
    Returns
    -------
    str
        The normalized station name
        
    Description
    -----------
    Replaces all punctuations by "_", removes consecutive "_" and removes last character if "_".
    
    """
    for ch in string.punctuation + " ":
        station_name = station_name.replace(ch,"_")
    station_name = re.sub("_+", "_", station_name)
    station_name = station_name.rstrip("_")
    station_name = station_name.lower()
    
    return station_name

 
def remove_flatlines(
    timeseries: pd.Series,
    threshold: int = 24, 
    inplace: bool = False,
) -> pd.Series:
    
    """
    Replace ranges with minimum 'threshold' consecutive equal values by NaN. In the solar context, 
    we most of the time use a threshold that corresponds to 24h, which depends on the timeseries
    time granularity.
    
    Parameters
    ----------
    timeseries: pd.Series
        Input timeseries, to remove flatlines
    threshold: int = 24
        Number of consecutive equal values to be detected as flatlines,
        and converted to NaN
    inplace: bool = False
        If True, performs operation inplace

    
    Returns
    -------
    pd.Series
        Output timeseries, with flatlines converted to NaN
    """

    # get start and end indices of each flatline as an n x 2 array
    isflat = np.concatenate(([False], np.isclose(timeseries.ffill().diff(), 0), [False]))
    isedge = isflat[1:] != isflat[:-1]
    flatrange = np.where(isedge)[0].reshape(-1, 2)

    if not inplace:
        timeseries = timeseries.copy()
    for j in range(len(flatrange)):
        if flatrange[j][1] - flatrange[j][0] >= threshold:
            timeseries.iloc[flatrange[j][0]:flatrange[j][1]] = np.nan
    return timeseries


def aligndropnull(
    test: pd.Series or pd.DataFrame,
    ref : pd.Series or pd.DataFrame,
    drop_ref_zero: bool = False,
) -> pd.Series:
    
    """
    Align test index to ref index. Drop values from test and ref,
    if test value is null and, if drop_ref_zero == True, if ref
    value is null.
    
    Parameters
    ----------
    test: pd.Series or pd.DataFrame
        Test timeseries
    ref: pd.Series or pd.DataFrame
        Reference timeseries
    drop_ref_zero: bool = False
        If True, drop also test and ref values if ref value is
        null

    
    Returns
    -------
    pd.Series
        Output test and reference timeseries, with index aligned 
        and dropped null values
    """

    if not test.index.equals(ref.index):
        test, ref = test.align(ref, axis=0)
    if isinstance(test, pd.DataFrame):
        test_notnull = test.notnull().all(axis=1)
    else:
        test_notnull = test.notnull()
    if drop_ref_zero is True:
        notnull = test_notnull & ref.replace(0, np.nan).notnull()
    else:
        notnull = test_notnull & ref.notnull()
    test, ref = test[notnull], ref[notnull]
    return test, ref
