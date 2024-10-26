

from schBD_print.str2D_image_processing.base import *
from schBD_print.str2D_image_processing.Lift_Twist import uplift, twist

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

            sections, walls, contents  = find_walls_infected (snippet, col_idx, inc , prime_spc)
            # sections [-1][-1] = len(snippet)  # replace -1 by actual value

            func = 0
            if contents[0] == -1 and contents[1] == 1:  #condition for uplift
                if len(set(contents[1:])) != 1:
                    print ('weird rendering done, now can\'t get out')
                    continue
                func = 1
                if _debug_view: print ( 'UPL')
            elif len(set(contents)) == 1:
                if _debug_view: print ( 'TWS')
                # continue
                func = 2
            else:
                print ('weird condition')
                # last_sp = last_sp_copy =  find_last_index(contents, -1)
                # if last_sp != None:
                #     last_sp += 1
                #     while ( last_sp < len(contents)):
                #         if contents [last_sp] != 1:
                #             break
                #         last_sp += 1
                #     if last_sp < len(contents): # if it less then sometihng bas happened
                #         pass
                #     else:
                #         pass #===
                #         last_sp = last_sp_copy
                #         contents = contents[ last_sp: ]
                #         sections = sections[last_sp: ]
                #         walls = walls[last_sp: ]

                #         # adjust other values  , normalize them
                #         origin = sections [0][0] -1

                #         lump_start = lump_start +origin

                #         prime_spc = [  prime_spc[kk] for kk, kk2 in enumerate(ls) if kk2>= origin]

                #         sections = [  (i2-origin, j2-origin)  for i2,j2 in sections ]

                #         snippet= _s_obj [lump_start: lump_end +2]

                #         view_str(snippet)

                #         func = 1


            # raise SystemExit()

            if func == 1:
                SS = uplift(_s_obj, snippet, col_idx, walls, sections, (lump_start, lump_end),prime_spc, inc, contents, False)
            elif func == 2:
                SS = twist(_s_obj, snippet, col_idx, walls, sections, (lump_start, lump_end),other_spc, inc, False)
            else:
                print ('No function ')
            12
            if type(SS) == list :
                # view_str(SS)
                _s_obj = build_lines (SS, False)
                _s_obj = str2D_strip(_s_obj)
                any_changed = True

            # return _s_obj

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
