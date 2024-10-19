#  finds the root of the graph using leaf pruning algorithm

print_flag = False

def prune_algo ( adjacency_list_tok ):
    nodes = []
    adj_nodes = []
    bond_type_list = []
    RES = {}

    for line in adjacency_list_tok:                       #   Create a list of lists for each node
        bond_type = line[0]                               #
        n1= line[1]                                       #
        n2= line[2]                                       #
                                                          #
        if n1 not in nodes:                               #
            nodes.append ( n1 )                           #
            adj_nodes.append ([])                         #
            bond_type_list.append([])                     #
            if n1.endswith('N') : RES[n1] = {}            #
            idx , need_to_add = -1 , True                 #
        else:                                             #
            idx = nodes .index(n1)                        #
            need_to_add = n2 not in adj_nodes [idx]       #
        if need_to_add ==  True:                          #
            adj_nodes [idx] .append (n2)                  #
            bond_type_list[idx].append (bond_type)        #
        # ------------------------------                  #
        if n2 not in nodes:                               #
            nodes.append ( n2)                            #
            adj_nodes.append ([])                         #
            bond_type_list.append([])                     #
            if n2.endswith('N') : RES[n2] = {}            #
            idx , need_to_add = -1 , True                 #
        else:                                             #
            idx = nodes .index(n2)                        #
            need_to_add = n1 not in adj_nodes [idx]       #
        if need_to_add == True:                           #
            adj_nodes [idx] .append (n1)                  #
            bond_type_list[idx].append (bond_type)        #
        # ------------------------------                  #
        if n1.endswith('N') and n2.endswith('N') :        #
            # print (RES[n1], RES[n2] , line)             #
            RES[n1][n2] = RES[n2][n1] = line[3]           #


    if print_flag :
        print (nodes)
        print('---------')
        print (adj_nodes )

    node_length = len(nodes)
    prune_depth_trf = [0] * node_length
    unsolved_stack = list(range ( node_length) )
    adjNodes_index = [0] * node_length
    level_depth_trf = [0] * node_length

    for idx in range (node_length):                       # Get all the indices so that access time is O(1)
        adjNodes_index[idx] = [0] * len ( adj_nodes [idx] )
        for idx2, i in enumerate( adj_nodes[idx] ) :
            idx3 = nodes.index (i)
            adjNodes_index [idx] [idx2] = idx3

    for idx in range (node_length):                       # Find leaf nodes and mark them
        if nodes[idx].endswith('C'):                      # if it's a component/ PU set it as Leaf node
            prune_depth_trf [idx] = 1                     # initial
            level_depth_trf [idx] = 1
            unsolved_stack.remove(idx)

    '''
    to find the root of the tree, we must use the pruning algorithm to cut the leaves and the lightest brances one by one
    it also detects the presence of cycles, but to a limited extent.
    we must run regular DFS after the pruning is done to check the cycle.
    but pruning helps find out the center which is the most dense node

    '''
    # print ('init ', prune_depth_trf)

    broken_edges = []
    flag = True
    # cycle_flag = False
    while ( flag ) :
        flag = False
        adjacent_values = [0]*len(unsolved_stack)
        prune_candidates = []
        for i,idx  in enumerate(unsolved_stack):
            adjacent_values[i] = adj_item_local = [ prune_depth_trf [ idx2] for idx2 in adjNodes_index[idx] ]
            adj_item_level_values = [ level_depth_trf [ idx2] for idx2 in adjNodes_index[idx] ]
            if adj_item_local.count(0 ) > 1  :
                flag = True
            else:  # adj_item_local.count(0 )  == 1 or 0
                level_depth_trf [idx] = max ( adj_item_level_values ) +1
                if len (adj_item_local) == 2: # ---------------   just a bypass , no branch here
                    prune_candidates.append([ idx, sum ( adj_item_local )  ])
                else:
                    prune_candidates.append([ idx, sum ( adj_item_local ) +1 ])
        for item in prune_candidates:
            idx, trf_value = item
            prune_depth_trf [ idx] = trf_value
            # level_depth_trf [idx] = 1
            unsolved_stack .remove (idx)
        if len(prune_candidates) == 0:
            print ('Cycle Present in graph, overriding.. ' )
            # cycle_flag = True
            all_trf_values = [ sum(val) for val in adjacent_values  ]   #
            min_val = min ( all_trf_values )                            # Find any minimum value trf
            i = all_trf_values.index (min_val)                          # Find it's first index
            broken_edges_temp = [ idx:= unsolved_stack [i] ]            #    #Find which edges are broken to make it a tree
            for j in adjNodes_index[idx]:                               #    #those edges won't be persued later
                if prune_depth_trf[j] == 0:                             #    #while printing
                    broken_edges_temp.append ( j )                      #    #
            broken_edges.append ( broken_edges_temp)                    #    #
            prune_depth_trf [ unsolved_stack [i] ] = trf_value          # override trf value
            unsolved_stack.pop ( i)                                     # remove it from next iteration

    return nodes, adj_nodes, prune_depth_trf , adjNodes_index, RES, bond_type_list, broken_edges, level_depth_trf


    # # #======================================================================================================
    # # if print_flag :
        # # print (prune_depth_trf)
        # # print (cycle_flag)

    # # '''
    # # the problem is i don't know if there is one cycle left or multiple,
    # # if multiple, then i don't want to break some valudable edges
    # # so running standard DFS algo to find the loops,
    # # find the 2 nodes having the most minimum degree in that cycle and cut their edge.

    # # '''

    # # if cycle_flag:
        # # cycle_count = prune_depth_trf.count (0)
        # # if cycle_count == 3:
            # # idx_list = [ x for x,i in enumerate( prune_depth_trf) if  i == 0 ]
            # # degree_ls = [ len( adj_nodes[i] ) for i in idx_list  ]
            # # idx_mx = idx_list .pop ( degree_ls.index( max( degree_ls ) ) )

            # # print (idx_mx)
            # # n1,n2 = idx_list
            # # d1 = sum( [ prune_depth_trf [ idx2] for idx2 in adjNodes_index[n1] if idx2 != n2 ] ) +1
            # # d2 = sum( [ prune_depth_trf [ idx2] for idx2 in adjNodes_index[n2] if idx2 != n1 ] ) +1
            # # prune_depth_trf [  n1 ] = d1
            # # prune_depth_trf [  n2 ] = d2
            # # d3 =  sum( [ prune_depth_trf [ idx2] for idx2 in adjNodes_index[idx_mx] ] ) +1
            # # prune_depth_trf [ idx_mx ] = d3


            # # net1= nodes[n1]
            # # net2= nodes[n2]

            # # adj_nodes[n1].remove ( net2 )
            # # adjNodes_index[n1].remove ( n2 )

            # # adj_nodes[n2].remove ( net1 )
            # # adjNodes_index[n2].remove ( n1 )

            # # del cycle_count
            # # del n1, n2, net1, net2, d1, d2, d3,idx_mx, idx_list, degree_ls


        # # else:
            # # print ('''

            # # Run standard DFS algo to get all the cycles and cut them
            # # most likely it's an error, so not doing that

            # # ''')
            # # raise SystemExit()




    # # # del line,  dependency_values,flag, i
    # # # del  cycle_flag, unsolved_stack, to_be_removed
    # # if print_flag :
        # # print (prune_depth_trf)
    # # # del  idx, idx2, idx3,





'''
do it before finding depth of the graph
otherwise depth calculation loop will not end


cut the smallest bridge
do it iteratively so that all loops are deleted



multple pull up problem


multiple links problem

--process RCM differently
-- same components  same color, even though they are located at different locations
-- can they be joined into one? such as RCm or PMIC


--for MSM,s GPIO are source
Poewr are the sink  how to define it ?

'''























