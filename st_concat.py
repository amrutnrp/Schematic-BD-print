# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 00:31:03 2024

@author: amrutnp
"""
# debug_flag= False
# from functions import *
from functions import insert_blank_col_get, insert_blank_row, opp_dir, swap_dir, idx_dir, build_lines, make_comp_block, make_cap_block, view_str, add_tape, pre_pad, str_2D, glue_string, idx_dir_2
from __init__ import box_comp_open_v3_top

done_nets= []
net_block = '─{}─'

adjNodes_index,bond_type_list, nodes, rev_LUT , RES, tok_2_block, broken_bonds =  '','','','', '', '', ''
def store_variables (_1, _2, _3, _4, _5, _6, _7):
    global adjNodes_index,bond_type_list, nodes, rev_LUT , RES, tok_2_block, broken_bonds
    adjNodes_index,bond_type_list, nodes, rev_LUT , RES, tok_2_block , broken_bonds= _1, _2, _3, _4, _5, _6, _7

def set_donenet (inp):
    global done_nets
    done_nets = inp

def get_donenet():
    return done_nets

#==============================================================================#==============================================================================
#==============================================================================#==============================================================================
#==============================================================================#==============================================================================


def ABC( net, dirn = 'w', res = '', adjacent_override = None, debug_arg = False, netName_override = ''):

    net2= rev_LUT [ net ] if netName_override == '' else netName_override

    node_idx = nodes.index(net)

    # dirn2 = opp_dir ( dirn )
    swap = swap_dir (dirn)
    idx_dir2 = idx_dir (dirn)
    idx_dir3 = idx_dir_2 (dirn)

    adjIdx_bondName_local = []
    cmp_gnd  = []
    cmp_open = []
    net_res = []
    net_blocks = []

    #=================  discover nodes in graph ===============================   1
    if adjacent_override == None:
        exclude_list = done_nets
    else:
        exclude_list = adjacent_override
    for adj_idx, bond_i in zip ( adjNodes_index [node_idx],  bond_type_list[node_idx]   ):
        if nodes[adj_idx] in exclude_list:  # discard already rendered nets
            continue
        adjIdx_bondName_local.append ( [adj_idx, bond_i ])

    #=================  discover elements : component, caps and net branches ==   2
    for adj_idx, bond_i in adjIdx_bondName_local:
        if bond_i == 'O' or  bond_i == 'P':
            cmp_open.append (adj_idx)
        elif bond_i == 'G':
            cmp_gnd .append (adj_idx)
        elif bond_i == 'B':
            net_res.append ( [ nodes [adj_idx], RES[nodes [adj_idx]] [ net]  ])
        else:
            print ( 'unsolved', nodes [adj_idx], bond_i)
    done_nets .append (net)
    #=====================   make the net part, add resistor if it's present  =  3

    source= net_block.format (net2)
    source = str_2D(source, 1)
    if res!='':
        res_b = tok_2_block[res ]
        res_b = str_2D(res_b, 1)
        # print ("--", res_b)
        if res_b[0][idx_dir2] == ' ':                  # 3 line resistor, but 1 line net
            # source.insert(0, ' '*len(source[0]))
            insert_blank_row(source)
        source = pre_pad(res_b, source, horizontal = True, pad_plus =True, dirn=dirn, swap= swap)

    #====================================  render the children ================   4


    cmp_gnd = [ nodes [i] for i in cmp_gnd ]
    cmp_open = [ nodes [i] for i in cmp_open ]

    L1, L2, L3 = len(cmp_gnd), len(cmp_open), len(net_res)

    if L1 != 0:
        C1= make_cap_block( cmp_gnd, tok_2_block ,30,dirn)

    if L2 != 0:
        C2= make_comp_block ( cmp_open, tok_2_block, 15, dirn)
        if L3 != 0:
            C2 = add_tape (  C2 , 'n' )                                        #
        else:
            pass                                                               # 0,[1, few, many], x

        #===================================   Lift source vs Component ====
        m_lvl_src = source [0][idx_dir2] == ' '
        # idx_2 = 1 if dirn =='w' else -2
        m_lvl_cmp = not( C2[0][idx_dir3] == '─'  or C2[0][idx_dir3] == glue_string  )

        if m_lvl_src ==True and m_lvl_cmp == False:
            insert_blank_row( C2 )
        elif m_lvl_src ==False and m_lvl_cmp == True:
            insert_blank_row( source )

        del m_lvl_cmp  # m_lvl_src used later

    if L3 != 0:
        for item in net_res:
            net_i , res_i = item
            bloc = ABC( net_i, dirn, res_i)
            net_blocks.append (bloc)

        net_block_master_str = ''
        if len(net_blocks) > 0:
            master_str = ''
            for bloc in net_blocks:
                master_str = pre_pad(master_str, bloc, horizontal= False, pad_plus =True, dirn=dirn)

            net_block_master_str = master_str


    #===================================   join the children to source net ====



    if   L1==0 and L2 ==0:                                                     #x,0,0
        C4 = source
    elif L1 !=0 and L2 ==0:                                                    #x,0,[1, few, many ]
        if source [0][idx_dir2] == ' ':
            # C1.insert(0, ' '*len(C1[0]))
            insert_blank_row(C1)
        C4 = pre_pad(source, C1, horizontal= True, pad_plus =True, dirn = dirn, swap= swap)
    elif L1 ==0 and L2==1 and L3 != 0:                                         #[1, few, many],1,0
        cmp_0 = cmp_open[0]
        cmp_0_name  = rev_LUT[cmp_0]
        single_comp=  box_comp_open_v3_top(cmp_0_name)
        #pad twice if source has resistor, or pad once
        single_comp= str_2D(single_comp, 1)
        single_comp = add_tape( single_comp, 'n')
        if m_lvl_src ==True: insert_blank_row( single_comp )
        C4 = pre_pad(source, single_comp , horizontal= True, pad_plus =True, dirn = dirn, swap= swap)
        del cmp_0, cmp_0_name,single_comp
    elif L1 ==0:                                                               #x,[few, many],0
        C4 = pre_pad(source, C2 , horizontal= True, pad_plus =True, dirn = dirn, swap= swap)
    else:
        w1 = len(source[0]); w2 = len(C2[0]) ; w3 = len(C1[0])
        w4 = w3 >> 1
        # make net source and capacitor list almost equal size
        if w3> w1:                                                             #
            ext_idx = idx_dir(opp_dir(dirn))  # take a bite from source and replicate it
            if not swap: # dirn == 'w':
                source =[ i+i[ext_idx]*(w3-w1) for i in source ]
            else:
                source =[ i[ext_idx]*(w3-w1)+ i for i in source ]

        if L2==1:                                                              #x, 1, x

            # C3 = pre_pad(source, C2 , horizontal= True, pad_plus =True, dirn = dirn, swap= swap)  ###
            # C4 = pre_pad(C3, C1 , horizontal= True, pad_plus =True, dirn = dirn)


            if L1 == 1 and L3 == 0:                                            # 0, 1,1
                #remove glue from top in case of single cap and single component
                # but if child net present, then keep it
                C1 = C1[1:]

            cap_overflow= False
            if w3 < w1+w2 and w4<w1 and w4<w2:
                left_pad = w1-w4
                right_pad = w2-w4
                latch_direction = dirn  # doesn't matter
            elif w3 < w1+w2 and w4 > w2 and w4 < w1:
                left_pad = w1+w2 - w3
                right_pad = 0
                # add good padding to net block
                latch_direction = opp_dir ( dirn )
            elif w3 < w1+w2 and w4 < w2 and w4 > w1:
                left_pad = 0
                right_pad = w1+w2-w3
                latch_direction = dirn
            else:               # capacitor too big for single component, let it have the space
                cap_overflow = True
            if cap_overflow== False:
                if swap:
                    left_pad, right_pad = right_pad, left_pad
                C1= insert_blank_col_get(C1, 'w', left_pad)
                C1= insert_blank_col_get(C1, 'e', right_pad)

                C3 = pre_pad(source, C2 , horizontal= True, pad_plus =True, dirn = latch_direction, swap= swap)  ###
                C4 = pre_pad(C3, C1 , horizontal= False, pad_plus =True, dirn = dirn)
            else:
                C3 = pre_pad(source, C1 , horizontal= False, pad_plus =True, dirn = opp_dir ( dirn ))
                C4 = pre_pad(C3, C2 , horizontal= True, pad_plus =True, dirn = dirn, swap= swap)
        else:  # many caps and many components.

            C3 = pre_pad(source, C1 , horizontal= False, pad_plus =True, dirn = opp_dir ( dirn ))
            C4 = pre_pad(C3, C2 , horizontal= True, pad_plus =True, dirn = dirn, swap= swap)


    if L3 != 0:
        m_lvl_child = not( C4 [0][idx_dir2] == ' ')
        # idx_2 = 1 if dirn =='w' else -2
        m_lvl_parent =  net_block_master_str [0][idx_dir3] == ' '
        if m_lvl_child ==True and m_lvl_parent == False:
            insert_blank_row( C4 )

            # net_block_master_str [0]
        elif m_lvl_child ==False and m_lvl_parent == True:
            insert_blank_row( net_block_master_str )
        del m_lvl_child, m_lvl_parent
        net_block_master_str = add_tape (  net_block_master_str , dirn )

        C5 = pre_pad(C4, net_block_master_str, horizontal= True, pad_plus =True, dirn= dirn, swap = swap)
    else:
        C5 = C4
    C6 = build_lines (C5, debug_arg)


#==============================================================================#==============================================================================
#==============================================================================#==============================================================================
#==============================================================================#==============================================================================
    if debug_arg:
        return C5
    else:
        return C6

