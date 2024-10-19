# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 00:31:03 2024

@author: amrutnp
"""
from string2D_functions import insert_blank_col_get, insert_blank_row, build_lines, make_comp_block, make_cap_block, view_str, add_tape, pad_join_2Dstr, str_2D, glue_string
from __init__ import box_comp_open_v3_top


net_block = '─{}─'


class SCH_plotter:
    def __init__(self):
        self.adjNodes_index,self.bond_type_list, self.nodes, self.rev_LUT , self.RES, self.tok_2_block, self.broken_bonds =  '','','','', '', '', ''
        self.done_nets= []

        # default direction values
        self.dirn           = 'w'
        self.opp_dir        = 'e'
        self.LR_swap_flag   = False
        self.idx1           = 0
        self.idx2           = 1
        self.opp_dir_idx1   = -1

    def set_system_data (self, adjNodes_index,bond_type_list, nodes, rev_LUT , RES, tok_2_block , broken_bonds):
        """
        Parameters
        ----------
        adjNodes_index : list of lists
            adjacency list
        bond_type_list : list of lists
            bond information stored in the skeletal format of adjacency list
        nodes : list
            contains node info, order equivalent to other lists
        rev_LUT : dict
            key is token and returns actual netname/resistor/component/capacitor
        RES : dict of dict
            put two nets as index , and it'll return the resistor between them, provided they are connected by one
        tok_2_block : dict
            contains blocks of basic elements: cap/component/series components
        broken_bonds : ??
            DESCRIPTION. ??

        Returns
        -------
        None.

        """
        self.adjNodes_index,self.bond_type_list, self.nodes, self.rev_LUT , self.RES, self.tok_2_block , self.broken_bonds= adjNodes_index,bond_type_list, nodes, rev_LUT , RES, tok_2_block , broken_bonds

    def set_donenet (self, inp):
        """
        Parameters
        ----------
        inp : list
            a blank list or a list of tokens
            tokens meaning the token for elements in the schematic

        Returns
        -------
        None

        """
        self.done_nets = inp

    # def get_donenet(self):
    #     return self.done_nets

    def set_expansion_direction(self, direciton_inp):
        self.dirn =  direciton_inp
        if direciton_inp == 'w':
            self.opp_dir        = 'e'
            self.LR_swap_flag   = False
            self.idx1           = 0
            self.idx2           = 1
            self.opp_dir_idx1   = -1
        else:
            self.opp_dir        = 'w'
            self.LR_swap_flag   = True
            self.idx1           = -1
            self.idx2           = -2
            self.opp_dir_idx1   = 0
#==============================================================================#==============================================================================
#==============================================================================#==============================================================================
#==============================================================================#==============================================================================


    def SCH_plot(self, net, res = '', adjacent_override = None, retain_glue = False, netName_override = ''):
        """
        retain_glue -> keeps glue character intact for debug


        """
        sf= self  # used for direction variables only

        net2= self.rev_LUT [ net ] if netName_override == '' else netName_override
        node_idx = self.nodes.index(net)

        adjIdx_bondName_local = []
        cmp_gnd  = []
        cmp_open = []
        net_res = []
        net_blocks = []

        #=================  discover nodes in graph ===============================   1
        if adjacent_override == None:
            exclude_list = self.done_nets
        else:
            exclude_list = adjacent_override
        for adj_idx, bond_i in zip ( self.adjNodes_index [node_idx],  self.bond_type_list[node_idx]   ):
            if self.nodes[adj_idx] in exclude_list:  # discard already rendered nets
                continue
            adjIdx_bondName_local.append ( [adj_idx, bond_i ])

        #=================  discover elements : component, caps and net branches ==   2
        for adj_idx, bond_i in adjIdx_bondName_local:
            if bond_i == 'O' or  bond_i == 'P':
                cmp_open.append (adj_idx)
            elif bond_i == 'G':
                cmp_gnd .append (adj_idx)
            elif bond_i == 'B':
                net_res.append ( [ self.nodes [adj_idx], self.RES[self.nodes [adj_idx]] [ net]  ])
            else:
                print ( 'unsolved', self.nodes [adj_idx], bond_i)
        self.done_nets .append (net)
        #=====================   make the net part, add resistor if it's present  =  3

        source= net_block.format (net2)
        source = str_2D(source, 1)
        if res!='':
            res_b = self.tok_2_block[res ]
            res_b = str_2D(res_b, 1)
            # print ("--", res_b)
            if res_b[0][sf.idx1] == ' ':                  # 3 line resistor, but 1 line net
                # source.insert(0, ' '*len(source[0]))
                insert_blank_row(source)
            source = pad_join_2Dstr(res_b, source,
                             horizontal= True, swap= sf.LR_swap_flag,
                             dirn=sf.dirn )

        #====================================  render the children ================   4


        cmp_gnd = [ self.nodes [i] for i in cmp_gnd ]
        cmp_open = [ self.nodes [i] for i in cmp_open ]

        L1, L2, L3 = len(cmp_gnd), len(cmp_open), len(net_res)

        if L1 != 0:
            C1= make_cap_block( cmp_gnd, self.tok_2_block ,30,sf.dirn)

        if L2 != 0:
            C2= make_comp_block ( cmp_open, self.tok_2_block, 15, sf.dirn)
            if L3 != 0:
                C2 = add_tape (  C2 , 'n' )                                        #
            else:
                pass                                                               # 0,[1, few, many], x

            #===================================   Lift source vs Component ====
            m_lvl_src = source [0][sf.idx1] == ' '
            # idx_2 = 1 if dirn =='w' else -2
            m_lvl_cmp = not( C2[0][sf.idx2] == '─'  or C2[0][sf.idx2] == glue_string  )

            if m_lvl_src ==True and m_lvl_cmp == False:
                insert_blank_row( C2 )
            elif m_lvl_src ==False and m_lvl_cmp == True:
                insert_blank_row( source )

            del m_lvl_cmp  # m_lvl_src used later

        if L3 != 0:
            for item in net_res:
                net_i , res_i = item
                bloc = self.SCH_plot( net_i, res_i)
                net_blocks.append (bloc)

            net_block_master_str = ''
            if len(net_blocks) > 0:
                master_str = ''
                for bloc in net_blocks:
                    master_str = pad_join_2Dstr(master_str, bloc,
                                         horizontal= False,  #swap= False
                                         dirn=sf.dirn)

                net_block_master_str = master_str

        #===================================   join the children to source net ====

        # if L1 ==0 and L2 ==1  and L3 == 0:
        #     view_str(C2)

        if   L1==0 and L2 ==0:                                                     #x,0,0
            C4 = source
        elif L1 !=0 and L2 ==0:                                                    #x,0,[1, few, many ]
            if source [0][sf.idx1] == ' ':
                # C1.insert(0, ' '*len(C1[0]))
                insert_blank_row(C1)
            C4 = pad_join_2Dstr(source, C1,
                         horizontal= True, swap= sf.LR_swap_flag,
                         dirn = sf.dirn )
        elif L1 ==0 and L2==1 and L3 != 0:                                         #[1, few, many],1,0
            cmp_0 = cmp_open[0]
            cmp_0_name  = self.rev_LUT[cmp_0]
            single_comp=  box_comp_open_v3_top(cmp_0_name)
            #pad twice if source has resistor, or pad once
            single_comp= str_2D(single_comp, 1)
            single_comp = add_tape( single_comp, 'n')
            if m_lvl_src ==True: insert_blank_row( single_comp )
            C4 = pad_join_2Dstr(source, single_comp ,
                         horizontal= True, swap= sf.LR_swap_flag,
                         dirn = sf.dirn )
            del cmp_0, cmp_0_name,single_comp
        elif L1 ==0:                                                               #x,[few, many],0
            C4 = pad_join_2Dstr(source, C2 ,
                         horizontal= True, swap= sf.LR_swap_flag,
                         dirn = sf.dirn,)
        elif L1 ==1 and L2==1 and L3 != 0:                                         #x,1,1
            # both component and cap must be hanging
            cmp_0 = cmp_open[0]
            cmp_0_name  = self.rev_LUT[cmp_0]
            single_comp=  box_comp_open_v3_top(cmp_0_name)
            single_comp= str_2D(single_comp, 1)
            single_comp = add_tape( single_comp, 'n')
            C3 = pad_join_2Dstr(C1, single_comp ,
                         horizontal= True, swap= sf.LR_swap_flag,
                         dirn = sf.opp_dir )
            C4 = pad_join_2Dstr(source, C3 ,
                         horizontal= True, swap= sf.LR_swap_flag,
                         dirn = sf.dirn,)
            # add hook
            l_c4 = len(C4[0])
            C4[0][l_c4 >> 1] = '┴'
            del cmp_0, cmp_0_name,single_comp
        elif L1 ==1:                                                               #x,x,1
            if m_lvl_src == True :
                insert_blank_row( C1 )
            C3 = pad_join_2Dstr(source, C1 ,
                         horizontal= True, swap= sf.LR_swap_flag,
                         dirn = sf.dirn )
            C4 = pad_join_2Dstr(C3, C2 ,
                         horizontal= True, swap= sf.LR_swap_flag,
                         dirn = sf.dirn )
        else:
            w1 = len(source[0]); w2 = len(C2[0]) ; w3 = len(C1[0])    # get width of cap, net, and components
            w4 = w3 >> 1
            # make net / source block almost equal size to cap block
            if w3> w1:
                ext_idx = sf.opp_dir_idx1  # take a bite from source and replicate it
                if not sf.LR_swap_flag: # dirn == 'w':
                    source =[ i+i[ext_idx]*(w3-w1) for i in source ]
                else:
                    source =[ i[ext_idx]*(w3-w1)+ i for i in source ]


            if L2==1:                                                              #x, 1, x
                if L1 == 1 and L3 == 0:                                            # 0, 1,1
                    # in case of single cap and single component  , remove top glue from cap block
                    # but if child net present, then don't do it, it won't look asthetic
                    C1 = C1[1:]

                # change cap block size appropriately
                cap_overflow= False
                if w3 < w1+w2 and w4<w1 and w4<w2:
                    left_pad = w1-w4
                    right_pad = w2-w4
                    latch_direction = sf.dirn  # doesn't matter, variable won't be used
                elif w3 < w1+w2 and w4 > w2 and w4 < w1:
                    left_pad = w1+w2 - w3
                    right_pad = 0
                    # add good padding to net block
                    latch_direction = sf.opp_dir
                elif w3 < w1+w2 and w4 < w2 and w4 > w1:
                    left_pad = 0
                    right_pad = w1+w2-w3
                    latch_direction = sf.dirn
                else:               # capacitor too big for single component, let it have the space
                    cap_overflow = True
                    latch_direction = sf.opp_dir   # why ???
                #============================================
                # can i use swap and latch_direction as a single indicaor of dirn ???
                if cap_overflow== False:
                    if sf.LR_swap_flag:
                        left_pad, right_pad = right_pad, left_pad
                    C1= insert_blank_col_get(C1, 'w', left_pad)
                    C1= insert_blank_col_get(C1, 'e', right_pad)

                    C3 = pad_join_2Dstr(source, C2,
                                 horizontal= True, swap= sf.LR_swap_flag,
                                 dirn = latch_direction )
                    C4 = pad_join_2Dstr(C3, C1,
                                 horizontal= False,  #swap= False
                                 dirn = sf.dirn)
                else:
                    C3 = pad_join_2Dstr(source, C1,
                                 horizontal= False,  #swap= False
                                 dirn =  latch_direction )
                    C4 = pad_join_2Dstr(C3, C2 ,
                                 horizontal= True, swap= sf.LR_swap_flag,
                                 dirn = sf.dirn )
            else:  # many caps and many components.
                C3 = pad_join_2Dstr(source, C1,
                             horizontal= False,  #swap= False
                             dirn = sf.opp_dir )
                C4 = pad_join_2Dstr(C3, C2,
                             horizontal= True, swap= sf.LR_swap_flag,
                             dirn = sf.dirn )


        if L3 != 0:
            # make net or source block equal height before joining
            m_lvl_child = not( C4 [0][sf.idx1] == ' ')
            m_lvl_parent =  net_block_master_str [0][sf.idx2] == ' '
            if m_lvl_child ==True and m_lvl_parent == False:
                insert_blank_row( C4 )
            elif m_lvl_child ==False and m_lvl_parent == True:
                insert_blank_row( net_block_master_str )
            del m_lvl_child, m_lvl_parent
            #add a mandatory glue in parent direction
            net_block_master_str = add_tape (  net_block_master_str , sf.dirn )

            C5 = pad_join_2Dstr(C4, net_block_master_str,
                         horizontal= True, swap= sf.LR_swap_flag,
                         dirn= sf.dirn )
        else:
            C5 = C4
        C6 = build_lines (C5, retain_glue)

    #==============================================================================#==============================================================================
        if retain_glue:
            return C5
        else:
            return C6

