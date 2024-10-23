
import pickle

import sys
from base import *
from Lift_Twist import uplift, twist
_this = sys.modules[__name__]
with open('s.pkl', 'rb') as f:
    S1, S2, S3 = pickle.load(f)

# del S1, S3
_s_obj = S2

_debug_view = True
debug_view1 = False

uplift_complete  = False

while(True):
    vert_lines = get_vertical_hooks(_s_obj)
    if _debug_view: view_str( _s_obj  )

    any_changed = False
    for V in vert_lines:
        lump_start, lump_end = V[1][0]
        col_idx = V[0]
        # string_hook = get_2D_col(_s_obj , V[0])
        # LR_indicator = string_hook[lump_end]
        LR_indicator = _s_obj [lump_end] [col_idx]
        if LR_indicator == '└':    inc = 1  # ('right leaned' )
        elif LR_indicator == '┘':  inc = -1 # ('left leaned' )
        else:
            print ('can\'t determine leaning orientaitons')
            continue
            raise SystemExit()

        ls = list(range (lump_start , lump_end + 1))   #includes both start and end
        lsl = list([0] * len(ls))
        lsr = lsl.copy()

        for idx, i in enumerate(ls):
            bef,af = find_neighbour_spaces( _s_obj[i], col_idx)
            lsr[idx] = af     if  af>3 else 0
            lsl[idx] = bef    if bef>3 else 0

        if lsl.count (0) == len(ls) == lsr.count (0) :
            # not much space left to do
            continue
        snippet = _s_obj [lump_start: lump_end +2]
        if inc == 1: # right sided
            prime_spc = lsr.copy()
            other_spc = lsl.copy()
        else:  # left sided
            prime_spc = lsl.copy()
            other_spc = lsr.copy()

        sections, walls, contents  = find_walls (snippet, col_idx, inc , prime_spc)
        sections [-1][-1] = len(snippet)  # replace -1 by actual value

        func = 0
        if contents[0] == -1 and contents[1] == 1:  #condition for uplift
            if len(set(contents[1:])) != 1:
                print ('weird rendering done, now can\'t get out')
                continue
            func = 1
            print ( 'uplift')


        elif len(set(contents)) == 1:
            print ( 'twist')
            func = 2
        else:
            print ('weird condition')
        print (col_idx,lump_end- lump_start, func)
        # raise SystemExit()
        h= input ('Enter y to confirm change ')
        if h == 'y':
            print ('step1')
            if func == 1:
                SS = uplift(_s_obj, snippet, col_idx, walls, sections, (lump_start, lump_end),prime_spc, inc, False)
            elif func == 2:
                SS = twist(_s_obj, snippet, col_idx, walls, sections, (lump_start, lump_end),other_spc, inc, False)
            else:
                print ('No function ')
                continue
            print ('step2')
            if SS != None:
                _s_obj = build_lines (SS, False)
                for n in dir():
                    if n[0]!='_' and  n!="_s_obj": delattr(_this, n)
                from base import *
                from Lift_Twist import uplift, twist

                break
            else:
                print ("None returned")
            # view_str( _s_obj  )

    print ('at while')









# print (walls)




