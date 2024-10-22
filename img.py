
import pickle


from base import * #Count_kch, find_lumps, get_2D_col, lump_thresh,find_neighbour_spaces, monotonize, find_walls, get_2D_area


with open('s.pkl', 'rb') as f:
    S1, S2, S3 = pickle.load(f)

# del S1, S3
_s_obj = S2

row,col = shape(_s_obj)
vert_lines = []
for i in range (0,col):
    each_col = get_2D_col(_s_obj, i )
    s = Count_kch(each_col)
    if s > lump_thresh:

        lumps = find_lumps ( each_col )
        if len(lumps) > 0:
            vert_lines.append ([i,lumps, s ])
del s,each_col, lumps, row, col, i, f
del lump_thresh

# print (vert_lines)
view_str( _s_obj  )

#============================================================================

# V = vert_lines[1]
# del vert_lines
# print (V)



# def find_wall_index(inp, start, inc):
#     limit = 0 if inc ==-1 else len(inp[0])
#     ptr = start + inc
#     for row in inp:
#         if ptr == limit:
#             break
#         column =  get_2D_col(inp, ptr)
#         all_chr = set(column)
#         all_ok = True
#         for ch in all_chr:
#             if ch not in wall_set:
#                 all_ok = False
#         if all_ok == True:
#             break
#         ptr += inc
#     return ptr



for V in vert_lines:
    SE = V[1][0]
    s = get_2D_col(_s_obj , V[0])
    col = V[0]


    LR_indicator = s[SE[1]]
    if LR_indicator == '└':
        LR ='right leaned'
        # print ('right leaned' )
        inc = 1
    elif LR_indicator == '┘':
        LR = 'left leaned'
        # print ('left leaned' )
        inc = -1
    else:
        print ('can\'t determine leaning orientaitons')
        continue
        raise SystemExit()


    ls = list(range (SE[0], SE[1]+1))
    lsl = list([0] * len(ls))
    lsr = list([0] * len(ls))

    for idx, i in enumerate(ls):
        bef,af = find_neighbour_spaces( _s_obj[i], col)
        lsr[idx] = af     if  af>3 else 0
        lsl[idx] = bef    if bef>3 else 0

    if lsl.count (0) == len(ls) == lsr.count (0) :   # not much space left to do
        continue
    strip = _s_obj [SE[0]: SE[1]+2]
    sections, walls, contents  = find_walls (strip, col, inc , lsr)


    if contents[0] == -1 and contents[1] == 1:
        if len(set(contents[1:])) != 1:
            print ('weird rendering done, now can\'t get out')
            continue
        print (LR, 'uplift')
        # continue

        if inc == 1: # right sided
            spacebar = lsr.copy()
        else:  # left sided
            spacebar = lsl.copy()



        sections [-1][-1] = len(_s_obj)  # replace -1 by actual value
        L= len(walls )
        order = list(range (1,L))
        record_height = [-1] * (L-1)
        axis_start = col
        space_row = sections[0][1] - 1
        row_sp, row_sectn = space_row,1


        ptr = 0 ; ptr2 = 1
        avl_h = 0;
        low_limit_row = 0

        while(row_sp > 0  and ptr < L-1 ):
            # get parameters
            row_sectn = order[ptr]
            H =sections[row_sectn][1]-  sections[row_sectn][0] +1
            W = walls[ row_sectn  ] - axis_start
            Avl_W = spacebar [row_sp]

            # print (H, W, Avl_W, avl_h, row_sectn)

            if  W <= Avl_W : # it fits !
                row_sp = row_sp - 1
                avl_h = avl_h + 1
                # decreasing_row = True
                # if avl_h >= H:
                if row_sp <= low_limit_row:
                    avl_h = 0
                    record_height[ ptr ] = row_sp
                    ptr += 1 ; ptr2 = ptr + 1
                    low_limit_row = row_sp + H
                    row_sp = max( row_sp + H, space_row)
            elif avl_h != 0  :
                avl_h = 0
                record_height[ ptr ] = row_sp+1
                ptr += 1  ; ptr2 = ptr + 1
                low_limit_row = row_sp + H
                row_sp = max( row_sp + H, space_row)
            elif row_sp > space_row:
                record_height[ ptr ] = record_height[ ptr -1 ] + H



                ptr += 1
                ptr2 = ptr + 1
            else:
                order[ptr], order[ptr2] = order[ptr2], order[ptr]
                ptr2 += 1

            # print ( ptr, ptr2, order,row_sp )
            # strip2 = strip.copy()
            # strip2 [ row_sp] = '*'*len(strip[0])
            # view_str(strip2)



        #Erase string section
        SS2= str_replace(_s_obj, col, col+1, ls[0]+1, ls[-1]+1, show = False)
        SS3= str_erase(SS2 , col+1, max(spacebar)+ col-1, sections[1][0], sections[-1][-1], show = False)

        # get sections
        snip = _s_obj [SE[0]: SE[1] +3]
        data_snip = []
        for i in range( L - 1):
            j = i+1
            data = get_2D_area(snip, col+1, walls[j] , sections[j][0], sections[j][1], False)
            data_snip.append (data)

        for i in range (L-1):
            SS3 = str_paste( SS3 , data_snip[i], ls[0] + record_height[i], col+1, False)

        # del data, S2, af, bef, contents, i, j, LR,LR_indicator,  lsl, lsr
        # # del ptr, ptr2, H, W, avl_h, Avl_W, row_sp, row_sectn, space_row, start, L, order
        # del wall_set, walls, snip, SE,
        view_str(SS3)



        continue

    elif len(set(contents)) == 1:
        print (LR, 'twist')
        continue

        if inc == 1: # right sided
            Content_side = lsr.copy()
            Space_side = lsl.copy()
        else:  # left sided
            Content_side = lsl.copy()
            Space_side = lsr.copy()

        sections2, walls2, contents2  = find_walls (strip, col, inc *-1 , lsl)







build_lines(SS3, True)



















