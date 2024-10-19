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
ls= [6]
LR_expansion = True


from string2D_functions import *
from __init__ import *
from SCH_plotter import SCH_plotter
# progress_bars = ['▂', '▅', '▇', '█']
progress_bars = ['▁', '▂', '▃', '▅', '▆', '▇', '▉' ]

class SCH_processor():
    def __init__(self):
        self.adj_list_data = []
        self.file_process_flag = False
        self.progress_counter = -1
    def nextstep(self):
        if self.progress_counter ==7:
            self.progress_counter = 0
        else:
            self.progress_counter += 1
        print (progress_bars[ self.progress_counter ], end='')

    def process_file(self, f_path):
        f= open (f_path ,'r')
        for line in f:
            _l1 = re.sub(r'\s+', '', line)
            _l2 =  _l1.split("*")
            self.adj_list_data.append(_l2)
        f.close()
        self.file_process_flag = True

    def start_processing(self):
        if self.file_process_flag == False:
            print ('File hsa not been read, no data present')
            return

        token_adj, rev_LUT, rev_LUT_int = tokenizer_nl_str(self.adj_list_data)
        self.nextstep()

        nodes, adj_nodes, prune_depth_trf , adjNodes_index, RES, bond_type_list , broken_edges, level_depth_trf = prune_algo(token_adj)
        self.nextstep()

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
        self.nextstep()
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

        plotter = SCH_plotter()
        plotter.set_system_data( adjNodes_index,bond_type_list, nodes, rev_LUT , RES, tok_2_block , broken_edges)
        plotter.set_donenet([])

        if ( len(_root_net) == 0 and LR_expansion == True) or LR_expansion == False: #single net
            net = nodes [ root_idx ]
            plotter.set_expansion_direction('w')
            x= plotter.SCH_plot(net, retain_glue= debug_flag)
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
            plotter.set_expansion_direction('e')
            S1 = plotter.SCH_plot(net, adjacent_override = right_wing,retain_glue= debug_flag , netName_override = '─')
            # _donenet =  get_donenet()
            # set_donenet(_donenet)
            plotter.set_expansion_direction('w')
            S2 = plotter.SCH_plot(net, adjacent_override = left_wing+_root_other ,retain_glue= debug_flag )
            # S11 = build_lines (S1, )
            # S22 = build_lines (S2, )

            S3 = pre_pad(S1, S2, horizontal = True, pad_plus = True, dirn = 'w')


        S9 = build_lines (S3 , False)

        S10 = str_2D(S9, 2)              #convert it into single string
        self.nextstep()
        make_web_page_nOpen (S10, openFlag = False)



        # h= input('press enter to continue')


for i in ls :
    obj = SCH_processor()
    obj.process_file( paths[i] )
    obj.start_processing()



