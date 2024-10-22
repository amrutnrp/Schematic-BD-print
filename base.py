# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 14:05:28 2024

@author: amrutnp
"""

lump_thresh = 4
vert_lut = tuple('├│┤└┘')

from schBD_print  import *

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

wall_set = '║ '


def find_walls(inp, start, inc,  space_bars ):
    limit = 0 if inc ==-1 else len(inp[0])-1


    sections = []
    contents = []
    ptrH= 0
    # find the horizontal subsections
    limH = len(inp) -1
    while(ptrH <= limH):
        if space_bars [ptrH] == 0:
            sections.append ( ptrH )
            if inp [ ptrH +1 ]  [ start +inc] != ' ':
                contents.append (1)
            else:
                contents.append (-1)
            ptrH += 3
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
        walls.append (ptr)

    return (sections, walls, contents)



def view_str(string):
    print ( '\n' .join (string ) )


def get_2D_area(string, col1, col2, row1, row2, show = False):
    S = [ row [col1:col2 ] for row in string [row1:row2]  ]
    if show== True : view_str(S)
    return S


def str_erase(string, col1, col2, row1, row2, show = False):
    S= string.copy()
    for row in range (row1, row2):
        S [row] = string[row][:col1] + ' '*(col2-col1) + string[row][col2:]

    if show== True : view_str(S)
    return S


def str_replace(string, col1, col2, row1, row2, show = False):
    S= string.copy()
    for row in range (row1, row2):
        S [row] = string[row][:col1] + '@'*(col2-col1) + string[row][col2:]

    if show== True : view_str(S)
    return S


def str_paste (str_canvas, str_small, row, col,  show = False):
    r,c = shape (str_small)
    String = str_canvas.copy()
    for row_i in range (r):
        i = row+row_i
        String[i] = String[i][:col]  + str_small[row_i] + String[i][col+c:]

    if show== True : view_str(String)

    return String








if __name__ == "__main__":



    inp = 'afsdghmjk. ├││┤└ qf├│┤└├│┤└'

    AA= find_lumps(inp)

    print (AA)



