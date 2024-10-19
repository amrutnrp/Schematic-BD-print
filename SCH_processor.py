# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 03:04:13 2024

@author: amrutnp
"""
import re

from string2D_functions import build_lines,str_2D, pad_join_2Dstr
from __init__ import *
from SCH_plotter import SCH_plotter
# progress_bars = ['▂', '▅', '▇', '█']
progress_bars = ['▁', '▂', '▃', '▅', '▆', '▇', '▉' ]


debug_flag = False
node_processing_threshold = 200

class SCH_processor():
    def __init__(self):
        self.adj_list_data = []
        self.file_process_flag = False
        self.progress_counter = -1
        self.pre_process_flag = False

        self.LR_expansion = True

    def nextstep(self):
        if self.progress_counter ==6:
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
        if len(self.adj_list_data) < node_processing_threshold:
            self.file_process_flag = True
        else:
            print ('can\'t read such a huge netlist')

    def make_globals(self):
        for name, value in self.__dict__.items():
            globals()[name] = value

    def get_view (self, option = 1):
        if self.pre_process_flag == False:
            print ('Pre processing not been done, can\'t proceed furthur')
            return []
        if option == 2: return self.S4
        else: return self.S5

    def pre_process(self):
        if self.file_process_flag == False:
            print ('File has not been read, no data present')
            return
        self.token_adj, self.rev_LUT, self.rev_LUT_int = tokenizer_nl_str(self.adj_list_data)
        self.nextstep()

        self.nodes, self.adj_nodes, self.prune_depth_trf , self.adjNodes_index, self.RES, self.bond_type_list , self.broken_edges, self.level_depth_trf = prune_algo(self.token_adj)
        self.nextstep()

        #======================================================================================
        self.series_elements_tok = [key for key in self.rev_LUT.keys() if key not in self.nodes]

        boxed_series_items  = {}
        component_box = {}
        for item in self.token_adj:
            if item[0] == "B":
                if len(item) != 4:  # Ensure the item has at least 4 elements
                    print ('bypass token item in token_adj has length != 4 ', item)
                    raise SystemExit()
                fourth_element = item[3]
                str_element = self.rev_LUT [fourth_element]
                boxed_series_items[ fourth_element ] = box_series( str_element )
                del fourth_element, str_element
            elif item[0] == "P":
                if len(item) != 4:  # Ensure the item has at least 4 elements
                    print ('pullup token item in token_adj has length != 4 ', item)
                    raise SystemExit()
                pu_res, comp = item[3], item[1]
                comp_element = rev_LUT [comp]
                res_element = rev_LUT [pu_res]
                component_box[ comp ] = [ box_pullup, comp_element, res_element ]
                del res_element, comp_element, pu_res, comp
        missing_keys = set(boxed_series_items.keys()) - set(self.series_elements_tok)
        if missing_keys:
            print("Keys in boxed_series_elements but not in series_elements:")
            for key in missing_keys:
                print(key)
            return -1
            # raise SystemExit()

        self.nextstep()
        #=======================================================================================

        for idx, i in enumerate(self.nodes):
            if i.endswith('C') : # if it's component
                str_element = self.rev_LUT [i]
                bond_temp = set( self.bond_type_list [idx] )
                if len(bond_temp) != 1:  # multiple types of bond not alllowed for a component
                    print (bond_temp , str_element)
                    print ('Multiple bond exists for a component {}'.format(str_element) )
                    raise SystemExit()
                bond_temp = list(bond_temp )[0]
                if bond_temp == "O":
                    component_box [ i ] = [ box_comp_open,  str_element ]
                elif bond_temp == "G":
                    component_box [ i ] = box_comp_PD( str_element)
                elif bond_temp == "P":
                    if i not in component_box.keys():
                        print ('Pullup element {} not found in component_box'.format(i))
                        raise SystemExit()
                del str_element
        #=======================================================================================
        self.nextstep()
        self.max_depth = max(self.prune_depth_trf)
        self.root_idx = self.prune_depth_trf.index ( self.max_depth )
        self.isnet =  tuple( [ True  if i_node.endswith('N') else i_node.endswith('R')  for i_node in self.nodes] )
        # RCM resisor node being counted as net  -- correct it later

        self.tok_2_block = {}

        for key, value in component_box.items():
            self.tok_2_block [ key ] = value
        for key, value in boxed_series_items.items():
            self.tok_2_block [ key ] = value

        del boxed_series_items, component_box, missing_keys, bond_temp
        del value, key, item,idx, i

        self.pre_process_flag = True
    def process_nPlot(self):
        if self.pre_process_flag == False:
            print ('Pre processing not been done, can\'t proceed furthur')
            return -1
        _ = self
        if max( _.level_depth_trf) > 4:
            _.LR_expansion = False
        else:
            _.LR_expansion = True
        #=====================================================================================
        #make dictionary fortok -> prune_depth_transfer value
        _.tok2_pval = { i:_.prune_depth_trf[idx] for idx,i in enumerate(_.nodes)  }

        #find_nets_only
        _._root_net= [ i  for i in _.adj_nodes[_.root_idx] if i.endswith('N') ]
        _._root_other =[ i  for i in _.adj_nodes[_.root_idx] if not i.endswith('N') ]

        plotter = SCH_plotter()
        plotter.set_system_data( _.adjNodes_index,
                                 _.bond_type_list,
                                 _.nodes,
                                 _.rev_LUT ,
                                 _.RES,
                                 _.tok_2_block ,
                                 _.broken_edges)
        plotter.set_donenet([])

        self.nextstep()

        if ( len(_._root_net) == 0 and _.LR_expansion == True) or _.LR_expansion == False: #single net
            net = _.nodes [ _.root_idx ]
            plotter.set_expansion_direction('w')
            _.S1= plotter.SCH_plot(net, retain_glue= debug_flag)
            _.S3 = build_lines (_.S1, False)
        else:
            _.net_pval = [ _.tok2_pval[i] for i in  _._root_net]
            _.n_combined = zip( _._root_net, _.net_pval)
            _.n_sorted = sorted(_.n_combined, key=lambda x: x[1], reverse=True)
            _._root_net2, _.net_pval2 = zip(*_.n_sorted)
            _._root_sum_thresh = sum( _.net_pval2 )  /2.5
            _.left_wing = []
            _.left_sum = 0
            for i in _._root_net2:
                if _.left_sum > _._root_sum_thresh:
                    break
                _.left_sum += _.tok2_pval [ i ]
                _.left_wing.append (i)

            _.right_wing = [ i for i in _._root_net if i not in  _.left_wing ]

            _.net = _.nodes [ _.root_idx ]
            plotter.set_expansion_direction('e')
            _.S1 = plotter.SCH_plot(_.net, adjacent_override = _.right_wing,retain_glue= debug_flag , netName_override = '─')
            plotter.set_expansion_direction('w')
            _.S2 = plotter.SCH_plot(_.net, adjacent_override = _.left_wing+_._root_other ,retain_glue= debug_flag )

            _.S3 = pad_join_2Dstr(_.S1, _.S2, horizontal = True, dirn = 'w')


        _.S4 = build_lines (_.S3 , False)

        _.S5 = str_2D(_.S4, 2)              #convert it into single string
        self.nextstep()
        #
        print ('')
