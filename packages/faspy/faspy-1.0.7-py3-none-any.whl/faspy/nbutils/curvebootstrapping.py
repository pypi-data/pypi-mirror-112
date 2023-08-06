import numpy as np
import numba

from collections import deque
from .nbdates import tenor_to_maturity as ttm, day_count_factor as day_cf, nb_datediff


def df_st(vdates, curves, day_count, business_day,
            rate_basis='Simple', holidays=[]):
    
    '''
    Calculate a series of historical discount factors
        Parameters:
            value_dates (list): list of datetime64 dates  
            curves (list): list of historical rates in dictionary containing tenor as rates
            day_count (str): day count convention
            business_day (str): business day convention
            rate_basis (str): rate basis

            Returns:
                list of dictionaries with the following keys - start_date, end_date, coupon, face_value, fv_flow

    '''

    # len of vdates and curves must be the same
    size = len(vdates)
    dfcurves = deque()
    for i in range(size):
        vdate = vdates[i]
        curve = curves[i]
        dfcurve = deque()
        for k in curve:
            tenor = {}
            tenor['tenor'] = k
            tenor['rate'] = curve[k]
            tenor['date'] = ttm(vdate, k, convention=day_count,
                                    business_day=business_day,
                                    holidays=holidays)
            tenor['dcf'] = day_cf(day_count, vdate, tenor['date'])
            tenor['time'] = day_cf('Actual/365', vdate, tenor['date'])
            tenor["days"] = (tenor["date"] - vdate).astype("int")
            if rate_basis == 'Simple':
                tenor['df'] = _mmr2df(tenor['rate'], tenor['dcf'])
            else:
                tenor['df'] = _dr2df(tenor['rate'], tenor['dcf'])
            dfcurve.append(tenor)
        dfcurves.append(list(dfcurve))
            
    return dfcurves


@numba.njit('float64(float64, float64)')
def _df2mmr(df, dcf):
    rate = ((1 / df) - 1) / (0.01 * dcf)
    return rate


@numba.njit('float64(float64, float64)')
def _mmr2df(rate, dcf):
    df = 1 / (1 + rate * 0.01 * dcf)
    return df


@numba.njit('float64(float64, float64)')
def _df2dr(df, dcf):
    rate = (1 - df) / (0.01 * df)
    return rate


@numba.njit('float64(float64, float64)')
def _dr2df(rate, dcf):
    df = 1 - rate * 0.01 * dcf
    return df