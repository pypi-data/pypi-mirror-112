#!/usr/bin/env python3

'''
Methods for univariate descriptive timeseries analysis.
'''

import pandas as pd
from pandas import Series

def simple_descriptive_analysis(series: Series) -> dict:
  '''
    Returns dictionary with TimeSeries specific features.
    This method generates a simple descriptive analysis of the timeseris data.
    TODO ...
    @param series: pd.Series
   
  '''
  result = {
    'min': series.min(),
    'mean': series.mean(),
    'median': series.median(),
    'max': series.max(),
    'std': series.std(),
    'var': series.var(),
    'largest': series.nlargest(),
    'smallest': series.nsmallest()
  }
  return result


####### TEST
if __name__ == '__main__':
  test_df = pd.Series(data=[0,1,2,3,4,5,6,3,2314,3,12,213,23,3,3,1])
  print(simple_descriptive_analysis(test_df))