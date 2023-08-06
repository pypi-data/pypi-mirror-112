import numba
import time
from numpy import datetime64 as dt64, timedelta64 as td64
import numpy

sdate1 = '2021-01-01'
sdate2 = '2022-01-01'
date1 = dt64('2021-01-01')
date2 = dt64('2022-01-01')
nbdate1 = numba.types.NPDatetime('D')(date1)
nbdate2 = numba.types.NPDatetime('D')(date2)
print(type(nbdate2))
i = 1
t = 1

def differences(date1,date2):
    return (date2 - date1).astype('int')/365

start0 = time.perf_counter()
for x in range(t):
    test1 = differences(date1, date2)
end0 = time.perf_counter()
print(f"Time taken is for test1 {end0-start0} seconds: result {test1}")

@numba.njit(numba.types.NPTimedelta('D')(numba.types.NPDatetime('D'), 
numba.types.NPDatetime('D')), cache = True)
def numba_differences2(date1, date2):
    a = (date2 - date1)
    return a

start0 = time.perf_counter()
for x in range(t):
    test2 = numba_differences2(date1, date2)
end0 = time.perf_counter()
print(f"Time taken is for test2 {end0-start0} seconds: result {test2}")


td_ayear = numba.types.NPTimedelta('D')(365)
#print(td_ayear)
@numba.njit(numba.float64(numba.types.NPDatetime('D'), numba.types.NPDatetime('D'),
numba.types.NPTimedelta('D')), cache = True)
def numba_differences3(date1, date2, thetime):
    a = (date2 - date1)
    c = a/thetime
    return c

start0 = time.perf_counter()
for x in range(t):
    test2 = numba_differences3(date1, date2, td_ayear)
end0 = time.perf_counter()
print(f"Time taken for test3  is {end0-start0} seconds: result {test2}")

# cant work with array of datetime64
@numba.njit(numba.types.NPTimedelta('D')(numba.types.NPDatetime('D')[:], 
numba.types.NPDatetime('D')[:]), cache = True)
def numba_differences4(date1, date2):
    size = len(date1)
    for i in range(size):
        a = date2[i] - date1[i]
    
    return a

start0 = time.perf_counter()
nbdates1 = numpy.fromiter((date1 for x in range(t)), '<M8[D]')
nbdates2 = numpy.fromiter((date2 for x in range(t)), '<M8[D]')

test2 = numba_differences4(nbdates1, nbdates2)
end0 = time.perf_counter()
print(f"Time taken for test4 is {end0-start0} seconds: result {test2}")

datemonth = dt64('2021-01-05', 'M')
month  = td64(6,'M')

@numba.njit(numba.types.NPDatetime('M')(numba.types.NPDatetime('M'), 
numba.types.NPTimedelta('M')), cache = True)
#@numba.jit
def movedatebymonth(date1, month):
    return date1 + (month)


@numba.njit(numba.types.NPDatetime('M')(numba.types.NPDatetime('M'), 
numba.types.int64), cache = True)
#@numba.jit
def movedatebymonth2(date1, month):
    return date1 + numba.types.NPTimedelta('M')(month)

start0 = time.perf_counter()
testdatemonth = movedatebymonth2(datemonth, 6)
end0 = time.perf_counter()
print(f"Time taken for testdatemonth is {end0-start0} seconds: result {dt64(testdatemonth,'D') + 5}")
