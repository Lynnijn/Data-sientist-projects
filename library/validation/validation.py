import numpy as np
import pandas as pd

from parsing import aligndropnull


# calculate validation metrics: mbe
def mbe(test, ref, drop_ref_zero=False):
    """ Mean Bias Error

    Parameters
    ----------
    test: pd.Series or pd.DataFrame
        Test data
    ref: pd.Series
        Reference data
    drop_ref_zero: bool, optional
        Default: False
    """
    test, ref = aligndropnull(test, ref, drop_ref_zero)
    return test.sub(ref, axis=0).mean()

# calculate validation metrics: nmbe
def nmbe(test, ref, norm='avg', drop_ref_zero=False):
    """ Normalized Mean Bias Error

    Parameters
    ----------
    test: pd.Series or pd.DataFrame
        Test data
    ref: pd.Series
        Reference data
    norm: 'avg' or float, optional
        Normalization value
    drop_ref_zero: bool, optional
        Default: False
    """
    test, ref = aligndropnull(test, ref, drop_ref_zero)
    if norm in ['avg', 'avg_nonzero']:
        norm = np.abs(ref.mean())
    return mbe(test, ref) / norm

# calculate validation metrics: rmse
def rmse(test, ref, drop_ref_zero=False):
    """ Root Mean Square Error

    Parameters
    ----------
    test: pd.Series or pd.DataFrame
        Test data
    ref: pd.Series
        Reference data
    drop_ref_zero: bool, optional
        Default: False
    """
    test, ref = aligndropnull(test, ref, drop_ref_zero)
    return np.sqrt((test.sub(ref, axis=0) ** 2.).mean())

# calculate validation metrics: nrmse
def nrmse(test, ref, norm='avg', drop_ref_zero=False):
    """ Normalized Root Mean Square Error

    Parameters
    ----------
    test: pd.Series or pd.DataFrame
        Test data
    ref: pd.Series
        Reference data
    norm: 'avg' or float, optional
        Normalization value
    drop_ref_zero: bool, optional
        Default: False
    """
    test, ref = aligndropnull(test, ref, drop_ref_zero)
    if norm == 'avg':
        norm = np.abs(ref.mean())
    return rmse(test, ref) / norm

# get summary values from validation metrics df
def get_summary_from_validation_metrics(
    df: pd.DataFrame,
    suffix = None,
):
    if suffix:
        row_index = f"summary_{suffix}"
    else:
        row_index = "summary"
    summary = pd.DataFrame(round(df.mean(), 2)).rename(columns={0: row_index}).transpose().rename(columns={"nmbe": "nmbe_avg"})
    summary["nmbe_std"] = round(np.std(df["nmbe"]), 2)
    summary["nbr_of_sites"] = len(df)
    summary["nbr_of_sites_hourly"] = df["nrmse_hourly"].count()
    custom_sort = {'nbr_of_sites': 1, 'nbr_of_sites_hourly': 2, 'nmbe_avg':5,'nmbe_std':6,'nrmse_yearly':7,'nrmse_monthly':8,'nrmse_daily':9,'nrmse_hourly':10,}
    summary = pd.DataFrame(summary, columns=sorted(custom_sort, key=custom_sort.get))
    
    return summary