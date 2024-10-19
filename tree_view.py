# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 17:05:50 2024

@author: amrutnp
"""
debug_flag = False
import os, re

s= os.listdir('data')
cwd = os.path.dirname(__file__)
paths = [ os.path.join ( cwd, 'data', i) for i in s ]
ls = range(len(paths))
ls= [9]
LR_expansion = True


from functions import *
from __init__ import *
from st_concat import store_variables, ABC, set_donenet, get_donenet

for i in ls :
    adj_list_data = []
    f= open (paths[i] ,'r')
    for line in f:
        _l1 = re.sub(r'\s+', '', line)
        _l2 =  _l1.split("*")
        adj_list_data.append(_l2)
    f.close()


    token_adj, rev_LUT, rev_LUT_int = tokenizer_nl_str(adj_list_data)
    print ('===')

    nodes, adj_nodes, prune_depth_trf , adjNodes_index, RES, bond_type_list , broken_edges, level_depth_trf = prune_algo(token_adj)
    print ('=== prune Done')

    #==================================================================================#
    series_elements_tok = [key for key in rev_LUT.keys() if key not in nodes]          #
                                                                                       #
    boxed_series_items  = {}                                                           #
    component_box = {}
    for item in token_adj:                                                             #
        if item[0] == "B":                                                             #
            if len(item) != 4:  # Ensure the item has at least 4 elements              #
                print ('bypass token item in token_adj has length != 4 ', item)        #
                raise SystemExit()                                                     #    Series bypass element process
            fourth_element = item[3]                                                   #
            str_element = rev_LUT [fourth_element]                                     #
            boxed_series_items[ fourth_element ] = box_series( str_element )           #====================
            del fourth_element
        elif item[0] == "P":                                                           #
            if len(item) != 4:  # Ensure the item has at least 4 elements              #
                print ('pullup token item in token_adj has length != 4 ', item)        #
                raise SystemExit()                                                     #    Pullup element process
            pu_res, comp = item[3], item[1]                                            #
            comp_element = rev_LUT [comp]                                              #
            res_element = rev_LUT [pu_res]                                             #
            component_box[ comp ] = [ box_pullup, comp_element, res_element ]          #
    missing_keys = set(boxed_series_items.keys()) - set(series_elements_tok)           #
    if missing_keys:                                                                   #
        print("Keys in boxed_series_elements but not in series_elements:")             #
        for key in missing_keys:                                                       #
            print(key)                                                                 #
        raise SystemExit()                                                             #
                                                                                       #
    # for i in boxed_series_items.values() :
    #     print (i)
    #======================================================================================#
                                                                                           #
    for idx, i in enumerate(nodes):                                                        #
        if i.endswith('C') : # if it's component                                           #
            str_element = rev_LUT [i]                                                      #
            bond_temp = set( bond_type_list [idx] )                                        #
            if len(bond_temp) != 1:  # multiple types of bond not alllowed for a component #   Component leafs done
                print (bond_temp , str_element)                                            #
                print ('Multiple bond exists for a component {}'.format(str_element) )     #
                raise SystemExit()                                                         #
            bond_temp = list(bond_temp )[0]                                                #
            if bond_temp == "O":                                                           #
                component_box [ i ] = [ box_comp_open,  str_element ]                      #
            elif bond_temp == "G":                                                         #
                component_box [ i ] = box_comp_PD( str_element)                            #
            elif bond_temp == "P":                                                         #
                if i not in component_box.keys():                                          #
                    print ('Pullup element {} not found in component_box'.format(i))       #
                    raise SystemExit()                                                     #
    #======================================================================================#
    print ("===  Leafs processed")
    max_depth = max(prune_depth_trf)
    root_idx = prune_depth_trf.index ( max_depth )
    isnet =  tuple( [ True  if i_node.endswith('N') else i_node.endswith('R')  for i_node in nodes] )
    # RCM resisor node being counted as net  -- correct it later

    tok_2_block = {}

    for key, value in component_box.items():
        tok_2_block [ key ] = value
    for key, value in boxed_series_items.items():
        tok_2_block [ key ] = value

    if max( level_depth_trf) > 4:
        LR_expansion = False
    else:
        LR_expansion = True
    #=====================================================================================
    #make dictionary fortok -> prune_depth_transfer value
    tok2_pval = { i:prune_depth_trf[idx] for idx,i in enumerate(nodes)  }

    #find_nets_only
    _root_net= [ i  for i in adj_nodes[root_idx] if i.endswith('N') ]
    _root_other =[ i  for i in adj_nodes[root_idx] if not i.endswith('N') ]
    store_variables( adjNodes_index,bond_type_list, nodes, rev_LUT , RES, tok_2_block , broken_edges)
    set_donenet([])

    if ( len(_root_net) == 0 and LR_expansion == True) or LR_expansion == False: #single net
        net = nodes [ root_idx ]
        x= ABC(net, dirn= 'w', debug_arg= debug_flag)
        S3 = build_lines (x, False)
    else:
        net_pval = [ tok2_pval[i] for i in  _root_net]
        n_combined = zip( _root_net, net_pval)
        n_sorted = sorted(n_combined, key=lambda x: x[1], reverse=True)
        _root_net2, net_pval2 = zip(*n_sorted)
        _root_sum_thresh = sum( net_pval2 )  /2.5
        left_wing = []
        left_sum = 0
        for i in _root_net2:
            if left_sum > _root_sum_thresh:
                break
            left_sum += tok2_pval [ i ]
            left_wing.append (i)

        right_wing = [ i for i in _root_net if i not in  left_wing ]

        net = nodes [ root_idx ]
        S1 = ABC(net, dirn='e', adjacent_override = right_wing,debug_arg= debug_flag , netName_override = '─')
        # _donenet =  get_donenet()
        # set_donenet(_donenet)
        S2 = ABC(net, dirn='w', adjacent_override = left_wing+_root_other ,debug_arg= debug_flag )
        # S11 = build_lines (S1, )
        # S22 = build_lines (S2, )

        S3 = pre_pad(S1, S2, horizontal = True, pad_plus = True, dirn = 'w')


    S9 = build_lines (S3 , False)

    S10 = str_2D(S9, 2)              #convert it into single string
    make_web_page_nOpen (S10, openFlag = False)

    # h= input('press enter to continue')






# dirn = 'w'

#

# store_variables( adjNodes_index,bond_type_list, nodes, rev_LUT , RES, tok_2_block , broken_edges)

# net = nodes [ root_idx ]
# x= ABC(net, dirn)
# # x= ABC('18N')
# # view_str(x)


# s = build_lines (x, True)
# s =

# make_web_page_nOpen (S10)




