
from operator import xor
from numpy import datetime64 as dt64, array as nparray, sum as npsum
from .nbdates import tenor_to_maturity as ttm, \
day_count_factor as day_cf
from .nbdates import generate_dates as gen_dates, nb_datediff, nb_datediff
from scipy import interpolate
import sympy as sy
import numba
import math
import time
from collections import deque
from .conventions import frequencies



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
                list of list of dictionaries with the following keys - tenor, rate, date, dcf, time,
                days and df for each tenor point [[{}]]
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
            tenor["days"] = int((tenor["date"] - vdate).astype("int"))
            if rate_basis == 'Simple':
                tenor['df'] = _mmr2df(tenor['rate'], tenor['dcf'])
            else:
                tenor['df'] = _dr2df(tenor['rate'], tenor['dcf'])
            dfcurve.append(tenor)
        dfcurves.append(list(dfcurve))

    return dfcurves


def generate_st_df_bymaturity(value_date, maturity, rate, convention,
                              business_day, rate_basis='Simple',
                              holidays=[]):
    result = {}
    dcf = day_cf(convention, value_date, maturity)

    time = day_cf('Actual/365', value_date, maturity)

    df = None
    if rate_basis == 'Money Market':
        df = 1/(1 + rate * 0.01 * dcf)
    elif rate_basis == 'Discount Rate':
        df = 1 - rate * 0.01 * dcf

    result['dates'] = maturity
    result['dcfs'] = dcf
    result['dfs'] = df
    result['times'] = time

    return result



def generate_fulldf(vdates, st_curves, st_daycount, st_business_day,
                    st_rate_basis, lt_curves, lt_daycount,
                    lt_business_day, frequency=6,
                    method="Forward from issue date",
                    holidays=[]):

    noofdates = len(vdates)
    # An array of ST discount factors
    sts_ = df_st(vdates, st_curves, st_daycount, st_business_day,
                    rate_basis=st_rate_basis)

    parrates_data = _convert_strates_toparrate(vdates, sts_, lt_business_day, lt_daycount,
                frequency)

    _combinedparrates(parrates_data, lt_curves, lt_daycount, lt_business_day, holidays=[])

    # an array of LT data with the same format as sts_ variable except for dcf and df keys
    new_ltcurves = _calc_lt_maturity(vdates,lt_curves, lt_daycount, lt_business_day, holidays)

    # place modified/calculated data from lt_curves parameter to dictionary in rates_data
    result = deque()
    for x in range(noofdates):
        vdate = vdates[x]
        ltcurve_fordate = new_ltcurves[x]
        stcurve_fordate = sts_[x]
        ori_parrates = parrates_data[x]['parrates']
        ori_partimes = parrates_data[x]['partimes']
        maturity = ltcurve_fordate[-1]['date']
        # generate all the coupon dates to obtain the par rate for each date
        # and subsequently calculate the discount factor
        cpndates = gen_dates(vdate, maturity, issueDate=vdate, frequency=frequency,
                            business_day=lt_business_day, method=method, holidays=[])
        lt_cpndates = cpndates.copy()
        len_dates = len(lt_cpndates)
        lt_cpnstarts = lt_cpndates[:len_dates - 1]
        lt_cpnends = lt_cpndates[1:]
        lt_days = [int(nb_datediff(vdate, lt_cpndate).astype("int"))
                        for lt_cpndate in lt_cpndates]

        lt_times = [day_cf('Actual/365', vdate, lt_cpnend) for lt_cpnend in lt_cpnends]
        lt_dcfs = list(map(lambda startdate, enddate: day_cf(lt_daycount, startdate,
                                        enddate, bondmat_date=maturity,
                                        next_coupon_date=enddate), lt_cpnstarts, lt_cpnends))

        interp_par = interpolation(ori_partimes, ori_parrates, 1, model='chip', is_function=True)
        # interpolated par rates for each coupon date
        lt_parrates = [float(interp_par(lt_time)) for lt_time in lt_times]

        # *********************************************************************
        #   BOOTSTRAPPING STARTS HERE
        # *********************************************************************
        full_time = parrates_data[x]['dftimes']
        full_dfs = parrates_data[x]['dfs']
        full_days = parrates_data[x]['days']

        lt_size = len(lt_times)
        # lt_dfs is to keep the discount factor for each coupon date
        lt_dfs = []
        #print(f"lt_days = {len(lt_days)} and lt_days = {lt_days}")
        #print(f"lt_times = {len(lt_times)} and lt_times = {lt_times}")
        for i in range(lt_size):

            ctime = lt_times[i]
            days = lt_days[i+1]
            par_rate = lt_parrates[i]
            # procedure if ctime IS within the current discount factor time range
            if ctime <= max(full_time):
                time_bool = [ctime == ptime for ptime in full_time]
                try:
                    # index return ValueError if value cant be found
                    # index error is handled in the except statement
                    index = time_bool.index(True)
                    lt_dfs.append(full_dfs[index])
                except:
                    time_bool = [ctime > ptime for ptime in full_time]
                    # find index of time which is the first to be more than ctime
                    index = time_bool.index(True)
                    idf = interpolation(full_time, full_dfs, ctime)
                    lt_dfs.append(idf)

            # procedure if ctime IS NOT within the current discount factor time range
            else:
                dcfs1 = nparray(lt_dcfs[:i])
                par_dfs = nparray(lt_dfs[:i])
                cpn_pv = dcfs1 * par_dfs * par_rate * 0.01
                #cpn_pv = list(map(lambda dcf, df: dcf * df * par_rate * 0.01,
                #                    dcfs1, par_dfs))
                values = npsum(cpn_pv)
                cdf = (1 - values) / (1 + par_rate * 0.01 * lt_dcfs[i])
                lt_dfs.append(cdf)
                full_time.append(ctime)
                full_dfs.append(cdf)
                full_days.append(days)
        result.append({"times": full_time, 'dfs': full_dfs, 'days': full_days})


    return result


def _rate_bootstrapping():
    pass


def _convert_strates_toparrate(vdates, strates, lt_business_day, lt_daycount, frequency):

    #using deques to make appending faster
    st2compound = convert_shortrate_to_compounding

    # processing the historical ST rates
    datasize =  len(vdates)
    result = deque()
    for x in range(datasize):
        strate = strates[x]
        vdate = vdates[x]
        par_rate = [st2compound(stpoint['rate'], vdate, stpoint['date'], frequency=12,
                                compound_busday=lt_business_day, compound_dc=lt_daycount,
                                compound_frequency=frequency) for stpoint in strate]
        par_rate.insert(0,0.0)
        par_time = [stpoint['time'] for stpoint in strate]
        par_time.insert(0, 0.0)
        df_time = [stpoint['time'] for stpoint in strate]
        df_time.insert(0, 0.0)
        df_df = [stpoint['df'] for stpoint in strate]
        df_df.insert(0, 1.0)
        df_date = [stpoint['date'] for stpoint in strate]
        par_date = df_date.copy()
        days = [nb_datediff(vdate, stpoint['date']).astype('int')  for stpoint in strate]
        days.insert(0,0)
        result.append({'value_dates': vdates, 'partimes': par_time, 'parrates': par_rate,
        'dftimes': df_time, 'dfs': df_df, "dfdates": df_date, 'pardates': par_date, 'days': days})

    return list(result)


def _combinedparrates(basedata, ltcurves, lt_daycount, lt_business_day, holidays=[]):
    # Processing the historical long term rates
    lts_ = deque()

    noofdates = len(basedata)
    for x in range(noofdates):
        ltcurve = ltcurves[x]
        vdate = basedata[x]['value_dates'][x]
        par_time = basedata[x]['partimes']
        par_rate = basedata[x]['parrates']
        par_date = basedata[x]['pardates']
        #par_days = basedata[x]['days']
        for k in ltcurve:
            rate = ltcurve[k]
            maturity = ttm(vdate, k, convention=lt_daycount,
                                    business_day=lt_business_day,
                                    holidays=holidays)
            timetomaturity = day_cf('Actual/365', vdate, maturity)
            noofdays = (maturity - vdate).astype("int")
            time_bool = [timetomaturity >= ptime for ptime in par_time]

            try:
                index = time_bool.index(False)
                if timetomaturity not in par_time:
                    par_time.insert(index, timetomaturity)
                    par_rate.insert(index, rate)
                    par_date.insert(index, maturity)
                    #par_days.insert(index, noofdays)

            except ValueError:
                if timetomaturity not in par_time:
                    par_time.append(timetomaturity)
                    par_rate.append(rate)
                    par_date.append(maturity)
                    #par_days.append(noofdays)


def _calc_lt_maturity(vdates, ltcurves, lt_daycount, lt_business_day, holidays=[] ):
    datasize = len(vdates)
    newltcurves = deque()
    for i in range(datasize):
        vdate = vdates[i]
        curve = ltcurves[i]
        newltcurve = deque()
        for k in curve:
            tenor = {}
            tenor['tenor'] = k
            tenor['rate'] = curve[k]
            tenor['date'] = ttm(vdate, k, convention=lt_daycount,
                                    business_day=lt_business_day,
                                    holidays=holidays)
            tenor['time'] = day_cf('Actual/365', vdate, tenor['date'])
            tenor["days"] = int((tenor["date"] - vdate).astype("int"))
            newltcurve.append(tenor)
        newltcurves.append(list(newltcurve))
    return newltcurves


def solver_rate_from_compounded_df(dis_factor,daycount_factors):
    rate = sy.Symbol('rate')
    fv = sy.Symbol('fv')
    #df = sy.Symbol('df')
    dcfs = daycount_factors
    #df = dis_factor

    for d in range(len(dcfs)):
        if d == 0:

            fv = (1 + (rate* 0.01*dcfs[d]) )
        else:
            fv = fv * (1 + (rate* 0.01*dcfs[d]) )

    fv = dis_factor * fv - 1

    solved_rates = sy.solveset(fv, rate, domain=sy.S.Reals)
    new_rates = []

    solved_rates = list(solved_rates)
    for i in range(len(solved_rates)):
        try:
            float(solved_rates[i])
        except:
            continue
        new_rates.append(solved_rates[i])

    new_rates = list(filter(lambda x: x>0, new_rates))
    return new_rates


def calc_fwd_df(start, end, time_axis=None, df_axis=None, ifunc=None):

    if ifunc is not None:
        df1 = ifunc(start)
        df2 = ifunc(end)
        return df2 / df1

    elif (time_axis is not None and df_axis is not None):
        interp = interpolation(time_axis, df_axis, start, is_function=True)
        df1 = interp(start)
        df2 = interp(end)
        return df2 / df1
    else:
        return None


def calc_shortrate_from_df(startdate, enddate, df, day_count,
                           rate_basis="Money Market"):
    sdate = dt64(startdate, "D")
    edate = dt64(enddate, "D")
    dcf = day_cf(day_count, sdate, edate, bondmat_date=edate,
                 next_coupon_date=edate)
    if rate_basis == "Discount Rate":
        return _df2dr(df, dcf)
    else:
        return _df2mmr(float(df), float(dcf))
    return None


def calc_df_from_shortrate(startdate, enddate, rate, day_count,
                           rate_basis="Money Market"):
    sdate = dt64(startdate, "D")
    edate = dt64(enddate, "D")
    dcf = day_cf(day_count, sdate, edate, next_coupon_date=edate)
    if rate_basis == "Discount Rate":
        return _dr2df(rate, dcf)
    else:
        return _mmr2df(rate, dcf)
    return None


def continuous_rate(value_date, rate, tenor, day_count="Actual/365",
                    rate_basis="Money Market"):
    maturity = ttm(value_date, tenor, convention=day_count)
    time = day_cf("Actual/365", value_date, maturity)
    dcf = day_cf(day_count, value_date, maturity)
    if rate_basis == "Money_Market":
        df = _mmr2df(float(rate), float(dcf))
    elif rate_basis == "Discount Rate":
        df = _dr2df(float(rate), float(dcf))

    crate = -math.log(df)/time
    return crate


def shift_curve(curve, bp=0.01):

    rates = dict(curve)
    for key in rates:
        rates[key] += bp
    return rates


def discount_factor_from_zspread(value_date, date_structure, day_count,
                                 frequency, df_curve, zspread):
    data = [{"start_date": x["start_date"], "end_date": x["end_date"]}
            for x in date_structure if value_date < x["end_date"]]

    x_axis = [x["times"] for x in df_curve]
    y_axis = [x["df"] for x in df_curve]
    ifunc = interpolation(x_axis, y_axis, 1/366, is_function=True)
    maturity = data[-1]["end_date"]
    zdfs = [{"times": 0, "df": 1}]
    for datum in data:
        if value_date > datum["start_date"]:
            time1 = day_cf("Actual/365", value_date, datum["end_date"],
                           bondmat_date=maturity,
                           next_coupon_date=datum["end_date"])
            df = ifunc(time1)
            fwd_rate = calc_shortrate_from_df(value_date,
                                              datum["end_date"],
                                              df, day_count)
            zfwd_rate = fwd_rate + zspread
            zfwd_df = calc_df_from_shortrate(value_date, datum["end_date"],
                                             zfwd_rate, day_count)
            zdfs.append({"times": time1, "zfwd_df": zfwd_df})

        else:
            start_time = day_cf("Actual/365", value_date,
                                datum["start_date"],
                                bondmat_date=maturity,
                                next_coupon_date=datum["end_date"])
            end_time = day_cf("Actual/365", value_date, datum["end_date"],
                              bondmat_date=maturity,
                              next_coupon_date=datum["end_date"])
            fwd_df = calc_fwd_df(start_time, end_time, ifunc=ifunc)
            fwd_rate = calc_shortrate_from_df(datum["start_date"],
                                              datum["end_date"],
                                              fwd_df, day_count)

            zfwd_rate = fwd_rate + zspread
            zfwd_df = calc_df_from_shortrate(datum["start_date"],
                                             datum["end_date"],
                                             zfwd_rate, day_count)
            zdfs.append({"times": end_time, "zfwd_df": zfwd_df})

    data_len = len(zdfs)

    for i in range(1, data_len, 1):

        datum = zdfs[i]
        pdatum = zdfs[i-1]
        datum["df"] = pdatum["df"] * datum["zfwd_df"]

    zdf_curve = [{"times": x["times"], "df": x["df"]} for x in zdfs]


    return zdf_curve

def convert_shortrate_to_compounding(rate, start, end, frequency=12,
                                     convention='Actual/365',
                                     compound_busday='No Adjustment',
                                     rate_basis='Money Market',
                                     compound_dc='Actual/365',
                                     compound_frequency=12,
                                     method="Forward from issue date"):
    result = None
    fre = 12/frequency
    compound_fre = 12/compound_frequency

    dcf = day_cf(convention, start, end, Frequency=fre)
    df = None
    if rate_basis == 'Money Market':
        df = 1/(1 + rate * 0.01 * dcf)
    else:
        df = 1-rate * 0.01 * dcf
    two_year_date = ttm(start, '2Y',
                                          convention=compound_dc,
                                          business_day=compound_busday,
                                          holidays=[])
    li_cpn_dcf = []

    dates = gen_dates(start, two_year_date, issueDate=start,
                               frequency=compound_frequency,
                               business_day=compound_busday,
                               method=method, holidays=[])

    no_of_cpn = len(dates)

    for cpn_no in range(no_of_cpn-1):
        prev_cpn = dates[cpn_no]
        next_cpn = dates[cpn_no +1]
        if end <= prev_cpn:
            break
        elif next_cpn >= end:
            cur_date = end
        else:
            cur_date = next_cpn

        cmp_dcf = day_cf(compound_dc,prev_cpn, cur_date,
                               bondmat_date = dates[-1], next_coupon_date = next_cpn,
                               business_day = compound_busday,
                               Frequency = compound_fre)
        li_cpn_dcf.append(cmp_dcf)

    result = solver_rate_from_compounded_df(df,li_cpn_dcf)
    result = float(result[0])

    return result


def interpolation(x_axis, y_axis, x_value, model='chip', method=None,
                  is_function=False):
    methods = ['linear', 'nearest', 'zero', 'slinear', 'quadratic', 'cubic',
               'previous', 'next']

    models = ['akima', 'chip', 'interp1d', 'cubicspline', 'krogh',
              'barycentric']

    result = None
    f = None
    if model is None or model == 'interp1d':
        if method in methods:
            f = interpolate.interp1d(x_axis, y_axis, kind=method)
        else:
            f = interpolate.interp1d(x_axis, y_axis, kind='cubic')

    elif model in models:
        if model == 'akima':
            f = interpolate.Akima1DInterpolator(x_axis, y_axis)

        elif model == 'chip':
            f = interpolate.PchipInterpolator(x_axis, y_axis)

        elif model == 'cubicspline':
            f = interpolate.CubicSpline(x_axis, y_axis)

        elif model == 'krogh':
            f = interpolate.KroghInterpolator(x_axis, y_axis)

        elif model == 'barycentric':
            f = interpolate.BarycentricInterpolator(x_axis, y_axis)
    else:
        f = interpolate.PchipInterpolator(x_axis, y_axis)

    if is_function == True:
        return f
    else:
        if not isinstance(x_value, list):
            # if x_value <min(x_axis) or x_value >max(x_axis):
            #    raise Exception('interpolation error: value requested is outside of range')
            #    return result
            try:
                result = float(f(x_value))
            except:
                return result

        else:
            result = list(map(lambda x: float(f(x)),x_value))

        return result


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
