# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 19:39:43 2019

@author: aaronliu
"""

import requests
from io import StringIO
import pandas as pd
import numpy as np

datestr = '20180328'
r = requests.get('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + datestr + '&type=ALL')
r.text[:1000]
# create dict 
df1 = {ord(c):None for c in ""}
df1
# use \n to split data
df2 = r.text.split('\n')
df2
# drop data that is not required 
df3 = [i.translate(df1)
       for i in df2
       if len(i.split('",'))==17 and i[0]!= '=']
df3
# join data by \n
df4 = "\n".join(df3)
df4
# store string into StringIO 
df5 = StringIO(df4)
df5
# use pd.read_csv to read data
df = pd.read_csv(df5, header=0)
df.head()
