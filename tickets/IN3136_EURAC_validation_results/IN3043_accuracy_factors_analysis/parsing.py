import os

import numpy as np
import pandas as pd

# detect daily shifts
def get_daily_shifts(measured, predicted, threshold=10):
    """ Get index shift of data, robustly detecting time shifts on a daily basis

    Parameters
    ----------
    measured : pd.Series
        data with potential time shift
    predicted : pd.Series
        reference data
    threshold : number, optional
        cumulative error threshold
        If 0, time shift is determined for each day independently
        If np.inf, a single optimal time shift will be obtained for the complete data series
        A threshold of 10 was found to be a good compromise for 15min irradiance data normalized to 1 (kW/m²).

    Examples
    --------
    Use case: messy data from FOSS, Cyprus
    >>> from library.degradation import get_daily_shifts, get_data, Degradation, get_formula, predict
    >>> data, meta = get_data('UCY_mono-C-Si-system-15min_2006-2016.csv')
    >>> deg = Degradation(data, meta=meta)
    >>> formula = get_formula('epi')
    >>> measured = deg._data['power']
    >>> predicted = predict(formula, data=deg._data)
    >>> get_daily_shifts(measured, predicted, threshold=1).plot()
    """
    measured = measured.fillna(0)
    predicted = predicted.fillna(0)
    # calculate daily aggregated absolute error for a range of index shifts
    shifts = pd.DataFrame(
        {i: (measured.shift(i) - predicted).abs().resample('D').sum()
         for i in [0, 1, -1, 2, -2, 3, -3, 4, -4]})
    shift_penalties = shifts.sub(shifts.min(axis=1), axis=0)
    groups = (shift_penalties.idxmin(axis=1).diff() != 0).cumsum()
    shift_penalties = shift_penalties.groupby(groups).transform('sum')
    weights = pd.Series(np.sort(shift_penalties, axis=1)[:, 1], index=shifts.index)
    best_shift = shift_penalties.idxmin(axis=1)
    # adjust threshold if needed to ensure that at least one weight reaches the threshold
    threshold = min(threshold, weights.max())
    shifts = best_shift.where(weights >= threshold)
    # fill gaps which have same value before and after (fill also start and end of series)
    shifts = shifts.ffill().bfill().where(shifts.ffill().bfill() == shifts.bfill().ffill())
    while shifts.isna().any():
        # we have to fill up gaps where before and after are different
        # fill up the heaviest weighted of best shifts in any gap
        shifts = shifts.fillna(best_shift.where(weights >= weights[shifts.isna()].max()))
        # fill gaps which have same value before and after
        shifts = shifts.ffill().where(shifts.ffill() == shifts.bfill())
    return shifts

# remove flatlines 
def remove_flatlines(ts, threshold=24, inplace=False):
    """ replace ranges with minimum `threshold` consecutive equal values by NaN
    """
    # get start and end indices of each flatline as an n x 2 array
    isflat = np.concatenate(([False], np.isclose(ts.ffill().diff(), 0), [False]))
    isedge = isflat[1:] != isflat[:-1]
    flatrange = np.where(isedge)[0].reshape(-1, 2)

    if not inplace:
        ts = ts.copy()
    for j in range(len(flatrange)):
        if flatrange[j][1] - flatrange[j][0] >= threshold:
            ts.iloc[flatrange[j][0]:flatrange[j][1]] = np.nan
    return ts