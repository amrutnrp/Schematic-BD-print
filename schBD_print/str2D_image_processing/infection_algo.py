# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 15:43:24 2024

@author: amrutnp
"""



def replace_str(X,idx,d):
    return X[:idx] + d+ X[idx+1:]
def view_str(string):
    print ( '\n' .join (string ) )

def view_mark(inp, row, col):
    inp2 = inp.copy()
    inp2[row] = replace_str(inp2[row] , col, "@")
    view_str(inp2)


infect_LUT = {
     '├':'─│',
     '─':'┤╢┬┐┘',
     '┤':'┌└',
     '└':'─',
     '┌':'─',
     '┘':'├',
     '┐':'├',

     '│':'└┼│├',
     '┼':'─│',
     '└':'─',
     '┬':'─┴│╧',

     '╢':'╔╚',
     '╚':'═',
     '╔':'═',
     '═':'╗╝',
     '╗':'║',
     '╝':'║',
     '┴':'─',
     '╧': '═'
     }

infect_LUT_H = {
     '├':'─',
     '─':'┤╢┬┐┘─',
     '└':'─',
     '┌':'─',

     '┼':'─',
     '└':'─',
     '┬':'─',

     '╚':'═',
     '╔':'═',
     '═':'╗╝═╛╘',
     '┴':'─',
     '╧': '═'
     }

infect_LUT_V = {
     '├':'│',
     '┤':'┌└',
     '┘':'├',
     '┐':'├',

     '│':'└┼│├',
     '┼':'│',
     '┬':'┴│╧',

     '╢':'╔╚',
     '═':'╗╝',
     '╗':'║',
     '╝':'║',
     }

def is_connecting_neighbour(seed_str, neigh ,horizontal = False):
    text_1 = seed_str.isalnum() == True or seed_str == "_" # seed_str in horizontally_ok
    text_2 = neigh.isalnum() == True or seed_str == "_"  # neigh in horizontally_ok


    if horizontal == True:
        if text_1 or text_2 :
            return True
        elif seed_str not in infect_LUT_H:
            return False
        elif neigh in infect_LUT_H[ seed_str ]:
            return True
        else:
            return False

    else:  # vertical
        if (text_2 and seed_str in '┴╧' ) or (text_1 and neigh in "═"):
             return True
        elif seed_str not in infect_LUT_V:
            return False
        elif neigh in infect_LUT_V[ seed_str ]:
            return True
        else:
            return False

    if seed_str not in infect_LUT:
        # print ('warning stuff ', seed_str, neigh)
        return False

    if neigh in infect_LUT[seed_str] :
        return True
    elif horizontal == True:
        # not letting these infect the paralell bars
        if seed_str == neigh and (seed_str=="═" or seed_str == "─" ):
            return True
        elif seed_str=="═"  and neigh in '╛╘':
            return True
        else:
            return False
    else:
        return False



class Infected_Boundary:
    def __init__(self, input_str, inc=1):
        self.next_idx = []
        self.col_current = 0
        self.col_str = ''
        self.inp_str = input_str
        self.inc = inc
        if inc == 1:
            self.Lrow = len(self.inp_str[0])
        else:
            self.Lrow =  0
    def col_check(self, seed, prev_seed = -5):
        seed_str = self.inp_str  [seed][self.col_current]
        # try:
        #     up, down, left = self.col_str[1+ seed-1], self.col_str[1+ seed+1], self.inp_str[ seed][self.col_current+self.inc]
        # except:
        #     view_str(self.inp_str)
        #     print (self.col_current)
        #     raise SystemExit()

        up, down  = self.col_str[1+ seed-1], self.col_str[1+ seed+1]

        if not self.col_current+self.inc == self.Lrow:
            left = self.inp_str[ seed][self.col_current+self.inc]
        else:
            left = ' '

        if seed_str == '╢':
            pass

        if prev_seed != seed-1 :
            A= is_connecting_neighbour(seed_str, up)
            # print ('A=',seed_str, up, A)
            if A== True:  self.col_check(seed-1, seed)
        if prev_seed != seed+1 :
            B= is_connecting_neighbour(seed_str, down)
            # print ('B=', down, B)
            if B==True:  self.col_check(seed+1, seed)


        C= is_connecting_neighbour(seed_str, left, horizontal= True)
        # print ('C=',left,  C)
        if C ==True:
            self.next_idx.append((prev_seed,self.col_current,seed))


    def define_col (self,col_idx):

        self.col_current = col_idx
        self.col_str =[ ' ']+ [ j [col_idx] for j in self.inp_str ]+[' ']


wall_set_infection = '║ ╗╝'

def track_infected(input_str, seed_col, seed_row, inc):

    S = Infected_Boundary(input_str,inc)


    S.next_idx = [(seed_col,seed_row)]


    max_col ,min_row , max_row = -1,10000,-1
    L = len(input_str[0])
    if inc==1:
        range_var = range(seed_col, L)
    else:
        range_var = range(seed_col, -1, -1)


    for col_i in range_var:
        nexxt = S.next_idx
        S.next_idx = []
        done_idx= []
        if len(nexxt) == 0:
            break
        max_col = max(max_col, col_i)
        for k in nexxt:
            if k[-1] in done_idx:
                continue
            # view_mark(inp, k[-1], col_i)
            # print(nexxt)
            done_idx.append (k[-1])
            S.define_col(col_i)
            S.col_check(  k[-1] )

            min_row, max_row = min(min_row, k[-1]), max(max_row, k[-1])
        # print (S.next_idx)
        # print ('==================================================================')

    col_last = set([ row[max_col] for row in input_str[min_row:max_row]  ])

    max_col += inc

    if inc==1:
        str_cut = [ row[seed_col:max_col] for row in input_str[min_row:max_row+1] ]
    else:
        str_cut = [ row[max_col-1:seed_col+1] for row in input_str[min_row:max_row+1] ]

    # view_str(str_cut)




    if any([ True if k not in wall_set_infection else False for k in col_last ])==True:
        print ("Blocked to move")
        return (-1, min_row, max_row, max_col, str_cut)
    else:
        return (1, min_row, max_row, max_col , str_cut)

if __name__ == "__main__":



#     inp = '''', '├', '│', '│'
# ── │ ╔═══════╗ │
# 53 ├─╢ U9582 ║ │
# ══╛│ ╚═══════╝ │
#    │ ╔═══════╗ │
#    ├─╢ U9579 ║ │
#    │ ╚═══════╝ │
#    │ ╔═══════╗ │
#    ├─╢ U9575 ║ │
#    │ ╚═══════╝ │
#    │ ╔═══════╗ │
#    ├─╢ U9532 ║ │
#    │ ╚═══════╝ │
#    │ ╔════════╗│
#    ├─╢ U12078 ║│
#    │ ╚════════╝│
#    │ ╔════════╗│
#    └─╢ TP9593 ║│
#      ╚════════╝│'''
#     inp = inp.split('\n')
#     # print(inp)
#     kk= track_infected(inp, 3+1, 2, 1)
#     print (kk)
#     view_mark(inp, kk[2], kk[3])

    import pickle

    import sys
    _this = sys.modules[__name__]
    with open('s.pkl', 'rb') as f:
        S1, S2, S3 = pickle.load(f)

    inp = S2[2:54]

    kk= track_infected(inp, 48+1, 30, 1)
    print (kk)

    kk= track_infected(inp, 48+1, 35, 1)
    print (kk)


    kk= track_infected(inp, 48+1, 45, 1)
    print (kk)


    kk= track_infected(inp, 48+1, 40, 1)
    print (kk)

    # inp = S2[50:]
    # kk= track_infected(inp, 48+1, 2, 1)


    kk= track_infected(inp, 48+1, 50, 1)
    print (kk)

    kk= track_infected(inp, 48+1, 19, 1)
    print (kk)

    kk= track_infected(inp, 48+1, 0, 1)
    print (kk)
