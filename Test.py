# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 17:05:50 2024

@author: amrutnp
"""

import os, re, time
from schBD_print import  *
s= os.listdir('data')
cwd = os.path.dirname(__file__)
paths = [ os.path.join ( cwd, 'data', i) for i in s ]
ls = range(len(paths))
ls= [6,7,8]
del s



for i in ls :

    obj = SCH_processor()
    obj.debug_flag = False
    obj.process_file( paths[i] )
    obj.pre_process()
    obj.process_nPlot()
    S= obj.get_view()
    # make_web_page_nOpen (S, openFlag = False)
    make_web_page_nOpen (S, openFlag = True, file_Path = 's_{}.html'.format (i))
    obj.make_globals()
    S4= obj.get_view(2)
    view_str(obj.S3)
    # time.sleep(1)



