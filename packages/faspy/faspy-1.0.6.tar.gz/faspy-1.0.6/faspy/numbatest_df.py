#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 13:36:21 2020

@author: RMS671214
"""
import time
from numpy import datetime64 as dt64
from nbutils.curvebootstrapping import df_st

# %%
rate_basis = "Simple"
day_count = "Actual/365"
bus_day = "No Adjustment"

rate ={'O/N': 2.30, '1W': 2.35, '1M': 2.45, '3M': 2.55, '6M': 2.65, '12M': 2.75}
date = dt64('2021-01-01', 'D')
x = 1000
rates = [rate for i in range(x)]
dates = [date for i in range(x)]

print(f"rates size is {len(rates)}")
start0 = time.perf_counter()
dfs = df_st(dates,rates,day_count, bus_day)
end0 = time.perf_counter()

print(f"Time taken is {end0-start0} seconds. Size is {len(dfs)}")


