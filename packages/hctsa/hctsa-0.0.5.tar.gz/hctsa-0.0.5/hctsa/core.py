#!/usr/bin/env python3

'''
This is the hctsa-core class.
Storing the timeseries data within a pandas DataFrame.
Interface to the different methods and classes of the hctsa-package.
'''

import pandas as pd

class HCTSACore:
  """HCTSA Core Class"""

  timeseriesData = pd.DataFrame()
  
  def __init__(self):
  ## TODO initialization: ...
    ...

  ######
  ## TimeSeries Data Pipeline
  ######

  def dataCleaning(self):
    ## Delete NaNs
    ## Fill NaNs with mean-all, zero, mean-border, ...
    ...

  def dataResampling(self):
    ## 1M, 15M, ...
    ...

  def splitData(self):
    ## Day, Week, ...
    ...

