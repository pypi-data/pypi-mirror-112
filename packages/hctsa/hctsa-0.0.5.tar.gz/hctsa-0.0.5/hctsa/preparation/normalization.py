#!/usr/bin/env python3

"""
Methods for normalization of timeseries data.
"""

from pandas import DataFrame

def standard(df: DataFrame) -> DataFrame:
  """
    Returns standard normalization of the TimeSeries data.
    @param df: pd.DataFrame
  """
  for col in list(df.columns):
    df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
  return df
  
def zscore(df: DataFrame) -> DataFrame:
  """
    Returns zscore normalization of the TimeSeries data.
    @param df: pd.DataFramee
  """
  for col in list(df.columns):
    df[col] = (df[col] - df[col].mean())/df[col].std(ddof=0)
  return df