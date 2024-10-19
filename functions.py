# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 12:01:16 2024

@author: amrutnp
"""

import numpy as np

glue_string = "@"

def validate_rect(string):
    if type(string) == str:
        str2 = string.split('\n')
        len_I = [   len(i) for i in str2]
    elif type(string) == list:
        len_I = [   len(i) for i in string]
    else:
        print ('FATAL error in rectangle check ')
    len_all = set (len_I )
    return True if len(len_all) == 1 else False


def str_2D(string, option = 1):
    """
    1 -> list of strings
    2 -> single string with \\n ; good for viewing
    3 -> numpy arrary string
    4 -> single string without \\n
    """
    if option == 1:
        if type(string) == str :
            str2 = string.split('\n')
        else:
            str2 = list(string)
        return str2
    # for option 2 and 3
    elif option == 2:
        if type(string) == str :
            str3 = str(string)
        else:  # type(string) == list
            str3 = '\n'.join(string)
        return str3
    # now only option 3 -- numpy
    else:
        if type(string) == str :
            str3 = string.replace('\n', '')
            L = string.find('\n')
        else:  # type(string) == list
            str3 = ''.join(string)
            L = len(string[0])
        # if option == 4: return str3
        arr1= np.array(list(str3))
        arr1.resize(  int(len(str3) / L ), L)
        return arr1

def pre_pad(str1, str2, horizontal = True, pad_plus = False, dirn = 'w', swap = False):
    A = str_2D (str1, 1)
    B = str_2D (str2, 1)
    if swap == True: A, B= B, A

    pad_ch = ' '
    if horizontal == True:  # assuming padding always done from south, in case of vertical stacking
        LA , LB = len(A) , len(B)
        if LA > LB:
            delta = LA- LB
            pad_str = delta* [ pad_ch* len(B[0])]
            B.extend(pad_str)
        elif LA < LB:
            delta = LB- LA
            pad_str = delta* [ pad_ch* len(A[0])]
            A.extend(pad_str)
        # merged with next function
        if pad_plus: return [ A[i]+B[i]  for i in range(len(A)) ]
    else:
        if pad_plus:
            if len(str1) == 1 and str1[0].strip()== '':
                return str2
            elif len(str2) == 1 and str2[0].strip()== '':
                return str1
        LA , LB = len(A[0]) , len(B[0])
        if LA > LB:
            delta = LA- LB
            pad_str = delta* pad_ch
            if dirn == 'w':
                for i in range (len(B)): B[i] += pad_str
            else:
                for i in range (len(B)): B[i] = pad_str + B[i]
        elif LA < LB:
            delta = LB- LA
            pad_str = delta* pad_ch
            if dirn == 'w':
                for i in range (len(A)): A[i] += pad_str
            else:
                for i in range (len(A)): A[i] = pad_str + A[i]
        if len(str1) == 1 and str1[0].strip()== '':
            return str2
        # merged with next function
        if pad_plus:
            if len(A) == 1 and A[0].strip()== '':
                return B
            if len(B) == 1 and B[0].strip()== '':
                return A
            return A + B
    return A, B

def join_2Dstr(str1, str2, horizontal = True):
    if horizontal == True:
        return [ str1[i]+str2[i]  for i in range(len(str1)) ]
    else:
        if len(str1) == 1 and str1[0].strip()== '':
            return str2
        return str1 + str2


def view_str(string):
    print ( '\n' .join (string ) )

def add_tape(string, side = 'n'):
    """  side can n, s ,w, e , for each direction """
    if len( string ) == 0 or len( string [0] ) == 0:
        return ''
    match (side):
        case ('n'):
            L =len( string [0] )
            return join_2Dstr ( [glue_string*L ], string, False )
        case ('w'):
            L = len( string )
            return join_2Dstr ( [glue_string]* L , string, True )
        case ('e'):
            L = len( string )
            return join_2Dstr ( string, [glue_string]* L , True )
        case _:
            L =len( string [0] )
            return join_2Dstr (  string,[glue_string*L ], False  )

def shape(string):
    return len(string), len(string [0])

def make_cap_block (cap_list , tok2_dict_local = {},  width_limit = 30 , dirn = 'w', child_flag= False):
    """
    cap_list: list of ground items in token form
    tok2_dict_local : the entire dictionary
    width limit : dpeends  ,but prefixed for now
    dirn: direction of parent
    """
    str_block = ['']
    comp_local = list(cap_list)
    level_ptr = 0
    # L =len(cmp_gnd)
    while (len(comp_local) > 0):
        cmp = comp_local.pop(0)
        # new_str_ln = tok2_dict_local [  cmp ] .split('\n')  # anyway being done in str2D
        new_str_ln = tok2_dict_local [  cmp ]


        str_iter = str_block [level_ptr]
        str_result = pre_pad(str_iter, new_str_ln, horizontal= True, pad_plus =True)
        # str_result = join_2Dstr(A, B, horizontal= True)
        str_block [level_ptr] = str_result
        if shape ( str_result ) [1] > width_limit:
            str_block.append ('')
            level_ptr += 1
    for i in range (len( str_block )):
        str_block[i] = add_tape (  str_block [i] , 'n')
        # view_str( str_block [i])
    else:
        if level_ptr > 0:
            master_str = ""
            for i in range (len( str_block )):
                master_str = pre_pad(master_str, str_block[i], horizontal= False, pad_plus = True, dirn = dirn)
                # master_str = join_2Dstr(A, B, horizontal= False)
            master_str = add_tape (  master_str , dirn )
        else:
            master_str = str_block[ 0 ]
            if child_flag: master_str = add_tape (  master_str , dirn )
    return master_str


def make_comp_block (comp_list , tok2_dict_local = {},  height_limit = 5 , dirn = 'w'):
    """
    comp_list: list of component items in token form
    tok2_dict_local : the entire dictionary
    height_limit : dpeends  ,but prefixed for now
    dirn: direction of parent
    """
    str_block = ['']
    comp_local = list(comp_list)
    level_ptr = 0
    # L =len(cmp_gnd)
    while (len(comp_local) > 0):
        cmp = comp_local.pop(0)
        # run the function wrt direction now
        func_list  = tok2_dict_local [  cmp ]


        dirn_arg = True if dirn == 'w' else False
        if len(func_list) == 2:
            new_str_ln = func_list[0] ( func_list[1] , dirn_arg)
        elif len(func_list) == 3:
            new_str_ln = func_list[0] ( func_list[1] ,func_list[2]  , dirn_arg)

        str_iter = str_block [level_ptr]
        str_result = pre_pad(str_iter, new_str_ln, horizontal= False, pad_plus =True, dirn = dirn)
        # str_result = join_2Dstr(A, B, horizontal= False)
        str_block [level_ptr] = str_result
        if shape ( str_result ) [0] > height_limit:
            str_block.append ('')
            level_ptr += 1

    for i in range (len( str_block )):
        str_block[i] = add_tape (  str_block [i] , dirn)
        # view_str( str_block [i])
    else:
        if level_ptr > 0:
            master_str = ""
            for i in range (len( str_block )):
                master_str = pre_pad(master_str, str_block[i], horizontal= True, pad_plus =True)
                # master_str = join_2Dstr(A, B, horizontal= True)
            master_str = add_tape (  master_str , 'n' )
        else:
            master_str = str_block[ 0 ]
    return master_str



boxchar_LUT= '   ┘ └─┴ │┐┤┌├┬┼'
# up_asking = [ '┐', '│' , '┌' , '┬' , '├' , '┤' , '┼', glue_string]
# left_asking = ['└' , '─' , '┌', '├', '┬' ,'┴' , '┼' , glue_string]
# right_asking = ['┐' , '─' , '┘', '┤', '┬' ,'┴' , '┼' , glue_string]
# down_asking = ['└' , '│' , '┘', '┴', '├' ,'┤' , '┼' , glue_string]

up_asking    = '┐│┌┬├┤┼' + glue_string
left_asking  = '└─┌├┬┴┼' + glue_string
right_asking = '┐─┘┤┬┴┼' + glue_string
down_asking  = '└│┘┴├┤┼╧' + glue_string

def build_lines( inp_string_array , debug_flag = False):
    # list only method : #LM
    # do padding
    w = len(inp_string_array[0]) +2
    h = len(inp_string_array) +2

    inp_starr_2 = [  ' '+seg+' ' for seg in inp_string_array]
    inp_starr_3 = ''.join(inp_starr_2)
    inp_starr_4 = ' '*w + inp_starr_3 + ' '*w
    #padding done

    unchecked_sym = [index for index, c in enumerate(inp_starr_4) if c == glue_string]
    pad_ar = list(inp_starr_4)
    del inp_starr_2, inp_starr_3, inp_starr_4

    # #=============== numpy method #NM

    # array1  = str_2D( C4, 3)
    # array2 = np.pad(array1, pad_width=1, mode='constant', constant_values=" ")
    # xy = np.where(array2==glue_string)

    # pad_ar_flat = array2.flatten()
    # pad_ar = list(pad_ar_flat)

    # # xy2 =  np.stack( (xy[0], xy[1] ), axis = 1)
    # x, y = list(xy[0]), list(xy[1])
    # xy3 = list (zip( x,y))
    # del xy, x, y

    # solved_indices = []
    # unchecked_sym = list ( xy3)
    # h,w = array2.shape
    # # xy2idx = lambda xy: xy[0]*w + xy[1] #NM

    sym_limit = 1
    # while (True):  #NM
    hollow_line_flag = False
    while(len(unchecked_sym) > 0):  #LM
        # if len(solved_indices) == len(unchecked_sym):  #NM
        #     break
        # if pad_ar.count ( glue_string ) == 0:
        #     break

        L1 = len(unchecked_sym)
        for k, i in enumerate(unchecked_sym):
            # if k in solved_indices: continue #NM
            # j = xy2idx ( i )  #NM
            j = i               #LM
            # nhbrs =  pad_ar[j-1-w: j+2-w] + pad_ar[j-1: j+2] + pad_ar[j-1+w: j+2+w]
            # reducing the size of slice, as corner cases don't matter, same for center case
            nhbrs =  pad_ar[j-w]+ pad_ar[j-1] + pad_ar[j+1] + pad_ar[j+w]
            if nhbrs.count (glue_string ) > sym_limit:
                continue

            U,D,L,R = 0,0,0,0
            if nhbrs [0]  in up_asking:     U = 1
            if nhbrs [1]  in left_asking:   L = 2
            if nhbrs [2]  in  right_asking: R = 4
            if nhbrs [3]  in  down_asking:  D = 8

            result = U+D+L+R
            # if result == 0:
            #     pad_ar [j] = ' '
            #     unchecked_sym.pop(k)
            #     print ('17263tgdbf')

            # elif hollow_line_flag == False:
            #     # skip_flag = True
            #     continue
            # else:
            result_ch = boxchar_LUT[result]
            if result_ch != ' ' and hollow_line_flag == False:
                continue
            pad_ar [j] = result_ch
            unchecked_sym.pop(k)
            # solved_indices.append(k)  #NM
            # unchecked_sym.pop(k)
            sym_limit = 1
            del U, L, D, R, j, nhbrs,

        # pad_ar = pad_ar_temp
        if L1 == len(unchecked_sym):
            if hollow_line_flag == False:
                hollow_line_flag = True
                continue
            print ('sym loop encountered')
            sym_limit = 2
        # del up_asking, left_asking, right_asking,down_asking



    pad_ar3 = ''.join(pad_ar)
    pad_ar4 = [  pad_ar3[i*w:(i+1)*w] for i in range (h) ]
    pad_ar5 = [  i[1:-1] for i in  pad_ar4 [1:-1]]  #remove padding
    if debug_flag: view_str (pad_ar5)

    return pad_ar5


opp_dir = lambda x: 'e' if x == 'w' else 'w'
swap_dir = lambda x: False if x == 'w' else True
idx_dir = lambda x: 0 if x == 'w' else -1

idx_dir_2 = lambda x: 1 if x == 'w' else -2

def insert_blank_row (string):
    string.insert(0, ' '*len(string[0]))
    # return not needed
def insert_blank_col_get(string, side, length ):
    if side == 'w':
        string2 = [ ' '*length + st for st in string ]
    else:
        string2 = [ st+ ' '*length  for st in string ]
    return string2


