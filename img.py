

from base import *
from Lift_Twist import uplift, twist

_debug_view = False
def improve_view(string):
    _s_obj = string.copy()
    any_changed = True
    while(any_changed == True):
        vert_lines = get_vertical_hooks(_s_obj)
        if _debug_view:
            view_str( _s_obj  )
                # print ( ptr, ptr2, order,row_sp )


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
                if _debug_view: print ('can\'t determine leaning orientaitons')
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
                if _debug_view: print ( 'UPL')
            elif len(set(contents)) == 1:
                if _debug_view: print ( 'TWS')
                func = 2
            else:
                print ('weird condition')
            # raise SystemExit()

            if func == 1:
                SS = uplift(_s_obj, snippet, col_idx, walls, sections, (lump_start, lump_end),prime_spc, inc, False)
            elif func == 2:
                SS = twist(_s_obj, snippet, col_idx, walls, sections, (lump_start, lump_end),other_spc, inc, False)
            else:
                print ('No function ')
            12
            if type(SS) == list :
                _s_obj = build_lines (SS, False)
                _s_obj = str2D_strip(_s_obj)
                any_changed = True

    return _s_obj


if __name__ == "__main__":

    import pickle

    import sys
    _this = sys.modules[__name__]
    with open('s.pkl', 'rb') as f:
        S1, S2, S3 = pickle.load(f)

    # del S1, S3
    # _s_obj = S2


    A= improve_view(S2)
    view_str(A)
