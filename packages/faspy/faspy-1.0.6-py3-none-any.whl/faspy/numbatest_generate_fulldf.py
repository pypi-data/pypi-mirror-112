#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 13:36:21 2020

@author: RMS671214
"""

from nbutils.nbcurves import generate_fulldf as gen_df
from numpy import datetime64 as dt64
import time

# %%
vdates = [dt64('2020-10-30')]
st_busday = 'Modified Following'
st_ratebasis = 'Simple'
st_daycount = 'Actual/365'
lt_busday = "No Adjustment"
lt_frequency =  "Semi-Annual"
lt_daycount = "Actual/Actual"

st_curves = [{'O/N': 2.30, '1W': 2.35, '1M': 2.45, '3M': 2.55,
                  '6M': 2.65}]
lt_curves = [{'1Y': 2.70, '2Y': 2.80, '3Y': 2.90}]
                  #'5Y': 3.00, '10Y': 3.10, '30Y': 3.25}]


start0 = time.perf_counter()
for i in range(2):
    dfs = gen_df(vdates, st_curves, st_daycount, st_busday,
                    st_ratebasis, lt_curves, lt_daycount,
                    lt_busday, frequency=6,
                    method="Forward from issue date",
                    holidays=[])
end0 = time.perf_counter()
print(f"Time taken is {end0-start0} seconds")
print(f"Total time = {len(dfs)} and dfs = {dfs}")
#print(dfs[0]['times'], len(dfs[0]['times']))
#print(dfs[0]['days'], len(dfs[0]['days']))
