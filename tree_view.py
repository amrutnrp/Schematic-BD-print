# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 17:05:50 2024

@author: amrutnp
"""

import os, re, time
from Debug_functions import *
s= os.listdir('data')
cwd = os.path.dirname(__file__)
paths = [ os.path.join ( cwd, 'data', i) for i in s ]
ls = range(len(paths))
# ls= [1]
del s

from SCH_processor import SCH_processor
from __init__ import *


for i in ls :
    obj = SCH_processor()
    obj.process_file( paths[i] )
    obj.pre_process()
    obj.process_nPlot()
    S= obj.get_view()
    # make_web_page_nOpen (S, openFlag = False)
    make_web_page_nOpen (S, openFlag = True)
    obj.make_globals()
    S4= obj.get_view(2)
    view_str(S4)
    time.sleep(1)



