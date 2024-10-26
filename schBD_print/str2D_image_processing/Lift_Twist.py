# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 11:52:11 2024

@author: amrutnp
"""
from schBD_print.str2D_image_processing.base import view_str, build_lines, str_erase, str_2D, str_paste, glue_string, get_2D_area, find_walls, str2D_mirror

def uplift(_s_obj, snippet, col_idx, walls, sections, lump_start_end,prime_spc, inc, contents, view_debug= False):

        L= len(walls)
        lump_start, lump_end = lump_start_end

        # strip = _s_obj [lump_start: lump_end +2]





        order = list(range (1,L))
        stopAt_level = [-1] * (L-1)

        space_row = sections[0][1] -1 +1
        row_sp, row_sectn = space_row,1

        ptr = 0 ; ptr2 = 1
        moving_up = False
        low_limit_row = 0
        prev_height = 0

        while(row_sp > 0  and ptr < L-1 and ptr2 < L-1 ):
            # get parameters
            row_sectn = order[ptr]
            H =sections[row_sectn][1]-  sections[row_sectn][0] +1
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
            if view_debug: print ('can\'t improve')
            # print ('can\'t improve')
            return -1
        #Erase string section
        SS2= str_erase(_s_obj, col_idx, col_idx+inc,  lump_start +1, lump_end+1, replaceBy= glue_string ) #,show = False)
        SS3= str_erase(SS2 , col_idx+inc, max(prime_spc)+ col_idx-inc, lump_start+ sections[1][0], lump_start +sections[-1][-1] +1) #, show = False)
        # using 2 here is controvercial ??
        # get sections
        snip = _s_obj [ lump_start: lump_end +2]
        data_snip = []
        for i in range( L - 1):
            j = i+1
            data = get_2D_area(snip, col_idx+inc, walls[j] , sections[j][0], sections[j][1] +1) #, False)
            data_snip.append (data)

        # overwrite sections
        for i in range (L-1):
            SS3 = str_paste( SS3 , data_snip[i], lump_start + stopAt_level[i] , col_idx+1 , False)

        SS3 = build_lines(SS3, False)

        # view_str(_s_obj)

        if view_debug: view_str(SS3)
        return SS3



def twist (_s_obj, snippet, col_idx, walls, sections, lump_start_end, other_spc, inc, view_debug= False):

        lump_start , lump_end = lump_start_end


        sections2, walls2, contents2  = find_walls (snippet, col_idx, inc*-1 , other_spc)
        # if debug_view: view_str( _s_obj  )
        if contents2[-1] != -1:
            if view_debug: print ('isolated - can\'t twist ')
            return -1


        L= len(walls)
        sections2 [-1][-1] = lump_end # replace -1 by actual value

        order = []
        stopAt_level = []

        row_sp= sections[-1][0] -1+1

        row_sectn = 0 # dummy
        ptr = L-1
        moving_up = False
        low_limit_row = 0
        while (True):
            # row_sectn = order[ptr]
            H =sections[ptr][1]-  sections[ptr][0]+1
            W = abs( walls[ ptr  ] - col_idx )
            Avl_W = other_spc [row_sp  ]

            if W < Avl_W:
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

        #------------------------------------------------------------------
        # get sections
        snip = _s_obj [ lump_start: lump_end +2]
        SS2 = _s_obj.copy()
        # view_str(snip)
        data_snip = []
        if order == []:
            return -2
        SS2= str_erase(SS2, col_idx, col_idx+inc, lump_start+1, lump_end+1, replaceBy= glue_string ) #,show = False)
        for j,i in  enumerate(order) :
            data = get_2D_area(snip, col_idx+inc, walls[i] , sections[i][0], sections[i][1] +1) #, False)
            data_snip.append (data)
            SS2= str_erase(SS2 , col_idx+inc, walls[i], lump_start+ sections[i][0], lump_start+ sections[i][-1]+1) #, show = False)
            DMir  = str2D_mirror( data )
            SS2 = str_paste( SS2 , DMir, lump_start + stopAt_level[j], col_idx+1-inc*len(data[0])-1) #, False)
        return SS2
