# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:05:28 2024

@author: amrutnp
"""
lump_thresh = 4
vert_lut = tuple('├│┤└┘')

from schBD_print.SCH.Debug_functions import view_str, validate_rect, shape
from schBD_print.SCH.string2D_functions import str_2D, build_lines, glue_string
from schBD_print.str2D_image_processing.infection_algo import track_infected, view_mark

def get_2D_col (String, col, rowslice = None):
    if rowslice == None:
        return [ row [col] for row in String ]
    else:
        rows =[ row [col] for row in String]
        return rows[rowslice[0]: rowslice[1]]

def Count_kch(col_list):
    sum_ = 0
    for char in vert_lut:
        sum_+= col_list.count (char)
    return sum_


class Interval():
    def __init__(self, start = 0):
        self.start = start
        self.end = start
    def inc(self):
        self.end += 1
    def diff(self):
        return self.end - self.start
    # def value(self):
    #     return self.start, self.end
    def __str__(self):
        return str(self.start) + ','+str( self.end)
    def value(self):
        """
        These can be used for indexing the first and last items
        """
        return self.start + 1, self.end


def find_lumps(input_list):
    # lumps = []
    lump_pts = []
    # current_lump = []
    current_lump = Interval()
    for idx,ch in enumerate(list(input_list)):
        if ch in vert_lut:
            current_lump.inc()
            # current_lump .append (ch)
        else:
            if current_lump.diff() > lump_thresh:
                # lumps.append (current_lump)
                lump_pts.append ( current_lump )
            current_lump = Interval(idx)
    if current_lump.diff() > lump_thresh:
        lump_pts.append ( current_lump )
    lump_pts = [ i.value() for i in lump_pts ]
    return lump_pts

def find_neighbour_spaces(inp,idx):
    count = 0
    before, after = 0,0
    for i in range ( idx+1, len(inp) ):
        if inp[i] != ' ': break
        after += 1
    for i in range ( idx-1, -1, -1 ):  # -1, to make the final as zero
        if inp[i] != ' ': break
        before += 1
    return before, after


def monotonize(arr_inp):
    arr= arr_inp.copy()
    L = len(arr)
    last = 0
    for i in range (L):
        if arr[i] < last :
            break
        last = arr[i]

    for j in range (i,L):
        arr[j]= 0
    return arr

# wall_H = {' ', '─', '┌', '┐', '═', '╔', '╗'}

wall_set = '║ ╗╝'
# wall_set = '║ '
connecting_str = '─'

def find_walls(inp, start, inc,  space_bars ):
    limit = 0 if inc ==-1 else len(inp[0])-1


    sections = []
    contents = []
    ptrH= 0
    # find the horizontal subsections
    limH = len(inp) -1
    branching_flag = False
    last_origin = 0
    while(True):
        if ptrH >= limH:
            if not branching_flag:
                sections.append( last_origin )
                if inp [ ptrH -1 ]  [ start +inc] != ' ':
                    contents.append (1)
                else:
                    contents.append (-1)
            break
        elif space_bars [ptrH] == 0 :
            sections.append ( ptrH )
            branching_flag = ( inp [ ptrH +1 ]  [ start +inc] == connecting_str )
            if inp [ ptrH +1 ]  [ start +inc] != ' ' :
                contents.append (1)
            else:
                contents.append (-1)
            ptrH += 3
            last_origin = ptrH
        else:
            ptrH += 1
    #===== sections discovered ============
    sections.append (  None)
    sections = [ [ sections[m] ,sections[m+1] ] for m in range(len(sections)-1) ]


    walls = []
    for section in sections:
        ptr = start + inc
        while (ptr <= limit):
            column =  get_2D_col(inp, ptr,  section )
            all_chr = set(column)
            all_ok = True
            for ch in all_chr:
                if ch not in wall_set:
                    all_ok = False
            if all_ok == True:
                break
            ptr += inc
        walls.append (ptr+inc)

    return (sections, walls, contents)

right_branching  = '├└'
left_branching = "┤┘"
def find_walls_infected(inp, start, inc,  space_bars ):
    limit = 0 if inc ==-1 else len(inp[0])-1
    # print ([ i[start] for i in inp])
    # view_str(inp)
    if inc==1:
        main_braching_list = right_branching
        reverse_branching_ls = left_branching
    else:
         reverse_branching_ls = right_branching
         main_braching_list = left_branching
    seed_list_1 = [ idx for idx,row in enumerate(inp) if row[start] in main_braching_list   ]
    seed_list_2 = [ idx for idx,row in enumerate(inp) if row[start] in reverse_branching_ls   ]

    if len (seed_list_1) != 0 and len (seed_list_2) == 0:
        seed_list = seed_list_1
    elif len(seed_list_2) != 0:
        if seed_list_1[0] > seed_list_2[-1]:
            seed_list = seed_list_1
        else:
            return [],[],[],[]
    else:
        print (seed_list_1, seed_list_2)
        return [],[],[],[]

    details = []
    for seed in seed_list:

        details_i = track_infected(inp, start+inc, seed, inc)
        details.append(details_i)

    sections = []
    contents = []
    walls = []
    snips = []

    id_start, id_end, id_ok, id_col, id_snip = 1,2,0,3, 4
    prev_section_end = -1
    ptr =  0

    while (ptr < len(details)):
        if details[ptr][id_start] == prev_section_end+1:
            sections .append( [ details[ptr][id_start] , details[ptr][id_end]  ])
            walls.append( details[ptr][id_col]  )
            if details[ptr][id_ok] == 1:
                contents .append(1)
            else:
                contents .append(-3)
            snips.append ( details [ptr][id_snip] )

            prev_section_end = details[ptr][id_end]
            ptr = ptr+1
        else: # encountered space area, unaccounted
            sections .append( [ prev_section_end+1 , details[ptr][id_start]-1  ])
            contents.append (-1)
            walls.append(-1)
            prev_section_end = details[ptr][id_start]-1
            snips.append ( [''] )



    # ptrH= 0
    # # find the horizontal subsections
    # limH = len(inp) -1
    # branching_flag = False
    # last_origin = 0
    # while(True):
    #     if ptrH >= limH:
    #         if not branching_flag:
    #             sections.append( last_origin )
    #             if inp [ ptrH -1 ]  [ start +inc] != ' ':
    #                 contents.append (1)
    #             else:
    #                 contents.append (-1)
    #         break
    #     elif space_bars [ptrH] == 0 :
    #         sections.append ( ptrH )
    #         branching_flag = ( inp [ ptrH +1 ]  [ start +inc] == connecting_str )
    #         if inp [ ptrH +1 ]  [ start +inc] != ' ' :
    #             contents.append (1)
    #         else:
    #             contents.append (-1)
    #         ptrH += 3
    #         last_origin = ptrH
    #     else:
    #         ptrH += 1
    # #===== sections discovered ============
    # sections.append (  None)
    # sections = [ [ sections[m] ,sections[m+1] ] for m in range(len(sections)-1) ]


    #
    # for section in sections:
    #     ptr = start + inc
    #     while (ptr <= limit):
    #         column =  get_2D_col(inp, ptr,  section )
    #         all_chr = set(column)
    #         all_ok = True
    #         for ch in all_chr:
    #             if ch not in wall_set:
    #                 all_ok = False
    #         if all_ok == True:
    #             break
    #         ptr += inc
    #     walls.append (ptr+inc)

    return (sections, walls, contents, snips)

def view_str(string):
    print ( '\n' .join (string ) )


def get_2D_area(string, col1, col2, row1, row2, show = False):
    """
    row col values are inclusive of both boundaries
    """
    if col1 > col2:
        col1, col2 = col2, col1
    S = [ row [col1:col2+1 ] for row in string [row1:row2+1]  ]
    if show== True : view_str(S)
    return S


def str_erase(string, col1, col2, row1, row2, replaceBy = ' ' ,show = False):
    """
    row col values are inclusive of both boundaries
    """
    S= string.copy()
    col22= col2+1
    row22 = row2+1
    substitute = replaceBy * (col22-col1)
    for row in range (row1, row22):
        S [row] = string[row][:col1] + substitute + string[row][col22:]

    if show== True : view_str(S)
    return S



def str_paste (str_canvas, str_small, row, col,  show = False):
    """
    row and col are inclusive of boundaries
    """
    if validate_rect(str_canvas) == False or validate_rect(str_small) == False:
        print ('BAD shape str_paste ')
        raise SystemExit()
    r,c = shape (str_small)
    String = str_canvas.copy()
    for row_i in range (r):
        i = row+row_i
        String[i] = String[i][:col]  + str_small[row_i] + String[i][col+c:]

    if show== True : view_str(String)

    return String

def is_blank_line (string):
    return string.strip() == ''
def get_vertical_hooks( String):
    """
    Parameters
    ----------
    String : List of strings
        2D string as input.

    Returns
    -------
    vert_lines : list
        Contains 3 items
            Column number
            [ row intervals  ];
        rowInterval is a tuple, item 0 and items 1 when indexed yield start and stop characters of vertical line

    """
    row,col = shape(String)
    vert_lines = []
    for i in range (0,col):
        each_col = get_2D_col(String, i )
        if '└' in each_col:
            lumps = find_lumps ( each_col )
            if len(lumps) > 0:
                vert_lines.append ([i,lumps ])
    return vert_lines

mirror_dict ={
        '╗':'╔',        '╔':'╗',
        '╝':'╚',        '╚':'╝',
        '╟':"╢",        '╢':'╟',
        '┌':'┐',        '┐':'┌',
        '└':'┘',        '┘':'└',
        '├':'┤',        '┤':'├',

        }

def str2D_mirror(string):
    arr=  []
    for row in string:
        s= ''
        temp = ''
        for ch in row:
            # print ( ch in mirror_dict)
            ch2 = mirror_dict[ch] if ch in mirror_dict else ch
            # print(ch)
            if ch.isalnum ():
                temp += ch
            else:
                if len(temp) != 0:
                    s= ch2 + temp + s
                    temp = ''
                else:
                    s = ch2 + s
        arr.append(s)
    # view_str(arr)
    return arr

def find_last_index (list_a, item):
    list_B = list_a.copy()
    list_B.reverse()
    if item in list_B:
        return len(list_B) - list_B.index (item ) - 1
    else:
        return -1


def str2D_strip(string):
    arr= []
    for row in string:
        if row.strip() != '':
            arr.append (row)
    arr2 = []
    col2_del = []
    for col in range(len(arr[0])):
        col_data = set([ row[col] for row in arr])
        if len(col_data) == 1 and col_data[0] == ' ':
            col2_del.append ()
    for row in arr:
        new_row_list  = [ ch for idx, ch in enumerate(row) if idx not in   col2_del    ]
        arr2.append ( ''.join(new_row_list))
    return arr2

if __name__ == "__main__":



    inp = 'afsdghmjk. ├││┤└ qf├│┤└├│┤└'

    AA= find_lumps(inp)

    print (AA)



