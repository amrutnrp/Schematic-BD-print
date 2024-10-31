# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 11:52:11 2024

@author: amrutnp
"""
from schBD_print.str2D_image_processing.base import view_str, build_lines, str_erase, str_2D, str_paste, glue_string, get_2D_area, find_walls, str2D_mirror, find_neighbour_spaces

def uplift(_s_obj, snippet, col_idx, walls, sections, lump_start_end,prime_spc, inc, contents,branch_snips, view_debug= False):

        L2 = len(prime_spc)
        lump_start, lump_end = lump_start_end

        # strip = _s_obj [lump_start: lump_end +2]

        #find status of each row
        row_wise_content = [0] *  L2
        row_wise_wall = [0] * L2
        for idx_s , section in enumerate (sections):
            for j in range (section[0] , section[1] +1 ):
                row_wise_content [ j ] =  contents[idx_s]
                row_wise_wall [j ] = walls [idx_s]

        #find space margins, assuming chirden aren't present
        space_alt = [0] *  len(prime_spc)
        for i in range (len(prime_spc)):
            if row_wise_content[i] == -1:
                space_alt[i] = prime_spc [i]
            elif row_wise_content[i] == 1:
                #now find the spaces beyond the wall
                wall_i = row_wise_wall [i]
                bef, af = find_neighbour_spaces (snippet[i], wall_i)
                space_alt[i] = wall_i + (af if inc ==1 else bef )
            else:
                #blocked area
                space_alt[i] = -3

        order = [i for i,Item in enumerate(contents) if contents[i] == 1 ]
        L= len(order)
        stopAt_level = [-1] * (L)

        row_sp = 0
        ptr = 0 ; ptr2 = 1

        prev_height = 0
        original_order = list(order)
        expt_flag = False

        while(row_sp < L2   and ptr < L ): #ptr2 < L
            # get parameters
            row_sectn = order[ptr]
            H =sections[row_sectn][1]-  sections[row_sectn][0] +1
            W = walls[ row_sectn  ] - col_idx
            Avl_W = space_alt [row_sp]

            if  W <= Avl_W : # the row fits !
                #check if whole section fits or not
                all_rows_4ThisSection = list(range(row_sp, row_sp+H ))
                fit_flag = [  True if W <= space_alt[i] else False for i in all_rows_4ThisSection ]

                if all(fit_flag) == True:
                    # yes, whole section fits
                    stopAt_level[ ptr ] = row_sp
                    ptr, ptr2 = ptr + 1, ptr + 2
                    row_sp = row_sp + H
                    # prev_height = H

                    original_order = order.copy()
                    expt_flag == False
                else:
                    # half of the section fits
                    # othre half is blocked by intruders or a branch blocked by intruders
                    pass
                    #try using the next block
                    order[ptr], order[ptr2] = order[ptr2], order[ptr]
                    ptr2 += 1
                    expt_flag = True
                # ptr, ptr2 = ptr + 1, ptr + 2
                # low_limit_row = row_sp + H +1
                # row_sp = max( row_sp + H, space_row)
                # prev_height = H
            else: # it doesn't fit
                if expt_flag == True and ptr2 == L:  # tried but failed, go to next row
                    row_sp = row_sp + 1
                    order = list(original_order)
                    expt_flag = False
                    ptr2 = ptr + 1
                else: # Try fitting the next block
                    #ptr2 < L
                    order[ptr], order[ptr2] = order[ptr2], order[ptr]
                    ptr2 += 1
                    expt_flag = True
            #stopAt_level[ ptr ] = stopAt_level[ ptr -1 ] + prev_height
            # prev_height = H

            # print ( ptr, ptr2, order,row_sp )
            # strip2 = strip.copy()
            # strip2 [ row_sp] = '*'*len(strip[0])
            # view_str(strip2)

        if ptr2 == L-1:
            if view_debug: print ('can\'t improve')
            # print ('can\'t improve')
            return -1
        # if all ( [ i==-1 for i in stopAt_level   ]) == True:
        if  -1 in stopAt_level:
            print ('Nothing changed')
            return -3
        #Erase string section
        SS3= str_erase(_s_obj, col_idx, col_idx,  lump_start , lump_end, replaceBy= glue_string ) #,show = False)
        # get sections
        snip = _s_obj [ lump_start: lump_end ]
        data_snip = []
        for i in range( L):
            #get the snip
            #indexing for section/content
            j = order[i]
            data = get_2D_area(snip, col_idx+inc, walls[j] -inc, sections[j][0], sections[j][1]) #, False)
            data_snip.append (data)

            #Erase previous area, in master canvas
            SS3 = str_erase ( SS3, col_idx+inc , walls[j]-inc, lump_start+ sections[j][0] ,  lump_start +sections[j][-1] , ' ')

        for i in range( L):
            #paste in new area
            # overwrite sections
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
        # data_snip = []
        if order == []:
            return -2
        SS2= str_erase(SS2, col_idx, col_idx, lump_start, lump_end, replaceBy= glue_string ) #,show = False)
        for j,i in  enumerate(order) :
            data = get_2D_area(snip, col_idx+inc, walls[i] -inc, sections[i][0], sections[i][1] ) #, False)
            # data_snip.append (data)
            SS2= str_erase(SS2 , col_idx+inc, walls[i] -inc, lump_start+ sections[i][0], lump_start+ sections[i][-1]) #, show = False)
            DMir  = str2D_mirror( data )
            SS2 = str_paste( SS2 , DMir, lump_start + stopAt_level[j], col_idx+1-inc*len(data[0])-1) #, False)
        return SS2
