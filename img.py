
import pickle
from base import *


with open('s.pkl', 'rb') as f:
    S1, S2, S3 = pickle.load(f)

# del S1, S3
_s_obj = S2

debug_view = True
debug_view1 = False

uplift_complete  = False

while(True):
    vert_lines = get_vertical_hooks(_s_obj)
    if debug_view1: view_str( _s_obj  )

    any_changed = False
    for V in vert_lines:
        lump_start, lump_end = V[1][0]
        col_idx = V[0]
        # string_hook = get_2D_col(_s_obj , V[0])
        # LR_indicator = string_hook[lump_end]
        LR_indicator = _s_obj [lump_end] [col_idx]
        if LR_indicator == '└':
            inc = 1
            # print ('right leaned' )
        elif LR_indicator == '┘':
            inc = -1
            # print ('left leaned' )
        else:
            print ('can\'t determine leaning orientaitons')
            continue
            raise SystemExit()

        del LR_indicator
        # del string_hook

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


        if uplift_complete  == False:
            if not (contents[0] == -1 and contents[1] == 1):  #condition for uplift
                continue
            if len(set(contents[1:])) != 1:
                print ('weird rendering done, now can\'t get out')
                continue
            # continue
            print (inc, 'uplift')

            #=================================================

            L= len(walls)


            order = list(range (1,L))
            stopAt_level = [-1] * (L-1)

            space_row = sections[0][1] - 1
            row_sp, row_sectn = space_row,1

            ptr = 0 ; ptr2 = 1
            moving_up = False
            low_limit_row = 0
            prev_height = 0

            while(row_sp > 0  and ptr < L-1 and ptr2 < L-1 ):
                # get parameters
                row_sectn = order[ptr]
                H =sections[row_sectn][1]-  sections[row_sectn][0]
                W = walls[ row_sectn  ] - col_idx
                Avl_W = prime_spc [row_sp]

                if  W <= Avl_W : # it fits !
                    row_sp = row_sp - 1
                    moving_up = True
                    if row_sp <= low_limit_row:
                        moving_up = False
                        stopAt_level[ ptr ] = row_sp
                        ptr, ptr2 = ptr + 1, ptr + 2
                        low_limit_row = row_sp + H +1
                        row_sp = max( row_sp + H, space_row)
                        prev_height = H
                elif moving_up == True:
                    moving_up = False
                    stopAt_level[ ptr ] = row_sp+1
                    ptr, ptr2 = ptr + 1, ptr + 2
                    low_limit_row = row_sp + H +1
                    row_sp = max( row_sp + H, space_row)
                    prev_height = H
                elif row_sp > space_row:
                    stopAt_level[ ptr ] = stopAt_level[ ptr -1 ] + prev_height
                    ptr = ptr + 1
                    prev_height = H
                else:
                    order[ptr], order[ptr2] = order[ptr2], order[ptr]
                    ptr2 += 1

                # print ( ptr, ptr2, order,row_sp )
                # strip2 = strip.copy()
                # strip2 [ row_sp] = '*'*len(strip[0])
                # view_str(strip2)

            if ptr2 == L-1:
                print ('can\'t improve')
                continue
            #Erase string section
            SS2= str_erase(_s_obj, col_idx, col_idx+inc, ls[0]+1, ls[-1]+1, replaceBy= glue_string ) #,show = False)
            SS3= str_erase(SS2 , col_idx+inc, max(prime_spc)+ col_idx-inc, ls[0]+ sections[1][0], sections[-1][-1] +ls[0]) #, show = False)
            # using 2 here is controvercial ??
            # get sections
            snip = _s_obj [ lump_start: lump_end +2]
            data_snip = []
            for i in range( L - 1):
                j = i+1
                data = get_2D_area(snip, col_idx+inc, walls[j] , sections[j][0], sections[j][1] ) #, False)
                data_snip.append (data)

            # overwrite sections
            for i in range (L-1):
                SS3 = str_paste( SS3 , data_snip[i], ls[0] + stopAt_level[i] , col_idx+1 , False)
            SS3 = build_lines(SS3, True)

            SS3 = build_lines(SS3, False)

            if debug_view1: view_str(SS3)
            _s_obj =  SS3
            #+=============================
            any_changed = True
            # break
            continue    # re-do all calculation before making any changes


        else:
            if not len(set(contents)) == 1:  # condition for twist
                continue
            print ( 'twist')
            continue

            sections2, walls2, contents2  = find_walls (snippet, col_idx, inc*-1 , other_spc)
            # if debug_view: view_str( _s_obj  )
            if contents2[-1] != -1:
                print ('isolated - can\t twist ')
                continue

            #=================================================

            L= len(walls)
            sections2 [-1][-1] = ls[-1] # replace -1 by actual value

            order = []
            stopAt_level = []

            row_sp= sections[-1][0] -1

            row_sectn = 0 # dummy
            ptr = L-1
            moving_up = False
            low_limit_row = 0
            while (True):
                # row_sectn = order[ptr]
                H =sections[ptr][1]-  sections[ptr][0]
                W = abs( walls[ ptr  ] - col_idx )
                Avl_W = other_spc [row_sp  ]

                if W< Avl_W:
                    row_sp = row_sp -1
                    if row_sp <= low_limit_row:
                        if moving_up == False:
                            break

                        else:
                            moving_up = False
                            stopAt_level .append (  row_sp )
                            order.append ( ptr)
                            ptr = ptr -1
                            low_limit_row = stopAt_level[-1] + H
                            row_sp =  sections[ptr][0] -1
                    else:
                        moving_up = True
                elif moving_up == True:
                    # snippet [ row_sp +1 ] = '@'*len(snippet[0])
                    moving_up = False
                    stopAt_level .append (  row_sp+1 )
                    order.append ( ptr)
                    ptr = ptr -1
                    low_limit_row = stopAt_level[-1] + H
                    row_sp =  sections[ptr][0] -1
                else:
                    break


                # if row_sp >= last_space:
                #     print ('233333333333333333333333333')

                # if row_sp >= reducing_height:
                #     stopAt_level.append( -11)
                    # break
                # else:
                #     break

                # print ( ptr, order,row_sp )
                # strip2 = snippet.copy()
                # strip2 [ row_sp] = '*'*len(snippet[0])
                # view_str(strip2)
                # print (ptr, order, stopAt_level, row_sp, H , low_limit_row)

            #----
            # get sections
            snip = _s_obj [ lump_start: lump_end +2]
            SS2 = _s_obj.copy()
            # view_str(snip)
            data_snip = []

            SS2= str_erase(SS2, col_idx, col_idx+inc, ls[0]+1, ls[-1]+1, replaceBy= glue_string ) #,show = False)
            for j,i in  enumerate(order) :
            #     j = i+1
                data = get_2D_area(snip, col_idx+inc, walls[i] , sections[i][0], sections[i][1] ) #, False)
                data_snip.append (data)
                # view_str(data)
                SS2= str_erase(SS2 , col_idx+inc, walls[i], ls[0]+ sections[i][0], sections[i][-1] +ls[0]) #, show = False)
                # view_str(SS2)
                DMir  = str2D_mirror( data )
                SS2 = str_paste( SS2 , DMir, ls[0] + stopAt_level[j], col_idx+1-inc*len(data[0])-1) #, False)
                # view_str(SS2)

            # print (lump_start, lump_end)
            SS2 = build_lines(SS2, False)
            _s_obj = SS2
            # break
        view_str(_s_obj)
    if any_changed == False:
        if uplift_complete  == False:
            uplift_complete  = True
            print ('uplift complete---------')
            # continue
        else:
            break


    # break















# print (walls)




