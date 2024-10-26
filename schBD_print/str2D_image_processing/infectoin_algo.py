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
     '─':'┤╢┬─┐┘',
     '┤':'┌└',
     '└':'─',
     '┌':'─',
     '┘':'├',
     '┐':'├',

     '│':'└┼│├',
     '┼':'─│',
     '└':'─',
     '┬':'─┴│',

     '╢':'╔╚',
     '╚':'═',
     '╔':'═',
     '═':'╗╝╛╘═',
     '╗':'║',
     '╝':'║',
     }

horizontally_ok = '_═─'

def is_connecting_neighbour(seed_str, neigh ,horizontal = False):
    text1 = seed_str.isalnum() == True or seed_str in horizontally_ok
    text2 = neigh.isalnum() == True or neigh in horizontally_ok
    if seed_str not in infect_LUT:
        if not text1:
            # print ('seed string not found')
            return False
    if (text1 or text2 ) :
        if horizontal == True:
            return True
        else:
            return False
    if neigh in infect_LUT[seed_str]:
        return True
    else:
        return False

class Infected_Boundary:
    def __init__(self, input_str):
        self.next_idx = []
        self.col_current = 0
        self.col_str = ''
        self.inp_str = input_str
        self.inc = 1

    def col_check(self, seed, prev_seed = -5):
        seed_str = inp [seed][self.col_current]
        up, down, left = self.col_str[1+ seed-1], self.col_str[1+ seed+1], self.inp_str[ seed][self.col_current+self.inc]



        A= is_connecting_neighbour(seed_str, up)
        B= is_connecting_neighbour(seed_str, down)
        C= is_connecting_neighbour(seed_str, left, horizontal= True)

        # print (seed_str, up, down, left, A,B,C ,self.col_current,seed )

        if prev_seed != seed-1 and A==True:  self.col_check(seed-1, seed)


        if prev_seed != seed+1 and B==True:  self.col_check(seed+1, seed)

        if C ==True:
            self.next_idx.append((prev_seed,self.col_current,seed))


    def define_col (self,col_idx):

        self.col_current = col_idx
        self.col_str =[ ' ']+ [ j [col_idx] for j in self.inp_str ]+[' ']


wall_set_infection = '║ ╗╝'

def fina_wall_infected(input_str, seed_col, seed_row, inc):

    S = Infected_Boundary(input_str)


    S.next_idx = [(1,5)]


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
            done_idx.append (k[-1])
            S.define_col(col_i)
            S.col_check(  k[-1] )

            min_row, max_row = min(min_row, k[-1]), max(max_row, k[-1])
        # print (S.next_idx)
        # print ('==================================================================')

    col_last = [ row[max_col] for row in input_str[min_row:max_row]  ]
    # print (min_row, max_row, max_col)
    # print (col_last)
    if any([ True if k in wall_set_infection else False for k in col_last ])==True:
        print ("Blocked to move")
        return (-1, min_row, max_row, max_col)
    else:
        return (1, min_row, max_row, max_col)

if __name__ == "__main__":



    inp = '''┬─┤ R10398 ├──BLEED_FETS_PU────┬─────┤ R10397 ├──BLEED_FETS_EN─┬──────────    -
    ┤ └────────┘                 ──┴──   └────────┘                │ ╔═══════╗      -
    │                            C474                              └─╢ Q9500 ║      -
    │                           ╘═════╛                              ╚═══════╝      -
    │ ┌────────┐                            ┌───────┐              ╔═══════╗        -
    ├─┤ R10335 ├──5V_PGOOD_ON─┬─────────────┤ R9873 ├──24V_PGOOD───╢ U9532 ║        -
    │ └────────┘   ╔════════╗ │ ╔═══════╗   └───────┘              ╚═══════╝        -
    │              ║ U12078 ╟─┼─╢ U9582 ║                           ╔═══════╗       -
    │              ╚════════╝ │ ╚═══════╝                           ║ Q9506 ╟─      -
    │                         │ ╔═══════╗                           ╚═══════╝       -
    │                         └─╢ U9575 ║                           ╔═══════╗       -
    │                           ╚═══════╝                           ║ Q9508 ╟─      -
    │                                                               ╚═══════╝ '''
    inp = inp.split('\n')
    # print(inp)
    kk= fina_wall_infected(inp, 5,1,1)
    print (kk)
    view_mark(inp, 4, 75)

