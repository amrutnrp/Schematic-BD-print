import re


write_toFile = False
dest_1 = 'token_to_element_string.md'
dest_2 = 'adjlist_with_token.md'


dict_elements, dict_reverse  = {}, {}
dict_reverse_int = ['']
counter = 0

f2 = ''

def add_glossary (a, flag):
    """
    flag is item type:
    C = Component
    N = Net
    S = Series item
    R = RCM
    """

    global dict_elements, dict_reverse, counter, f2, dict_reverse_int
    if a in dict_elements.keys():
        return dict_elements[a]
    else:
        counter = counter + 1
        id_ = str(counter) + flag
        dict_elements[a] = id_
        dict_reverse [ id_ ] = a
        dict_reverse_int.append (a)
        if write_toFile : f2.write (id_+'*'+a+'\n')
        return id_


def tokenizer_nl_str ( adj_list_data  = [] ):
    """
    Returns Ajdacency list where elements are tokens, token id
    and A dictionary where tokens can be translated to original items


    """

    data1 = adj_list_data

    global dict_elements, dict_reverse, counter, f2, dict_reverse_int


    dict_reverse = {}
    dict_elements = {}
    dict_reverse_int= ['']
    counter = 0

    data2 = []

    if write_toFile:
        f2 = open(dest_1 , 'w')
        f= open (dest_2, 'w')

    for i in data1:
        if i[2] == 'O':
            i1 = add_glossary ( i[0], 'C' )
            i2 = add_glossary ( i[1], 'N' )
            data2.append (['O', i1, i2])
        elif i[2] == 'GND':
            i1 = add_glossary ( i[0] ,'C')
            i2 = add_glossary ( i[1] ,'N')
            data2.append (['G', i1, i2])
        elif 'PU' in i[2]:
            i1 = add_glossary ( i[0] ,'C')
            i2 = add_glossary ( i[1] ,'N')
            i2 = add_glossary ( i[2] ,'S')
            data2.append ( ['P',i1, i2, i[2]])
        elif i[2] == 'RCM':
            i1 = add_glossary ( i[0] ,'R')
            i2 = add_glossary ( i[1] ,'N')
            data2.append ( ['R',i1, i2])
        else:
            i1 = add_glossary ( i[0] ,'N')
            i2 = add_glossary ( i[1] ,'N')
            i3 = add_glossary ( i[2] ,'S')
            data2.append (['B', i1, i2, i3])

        if write_toFile: f.write( ','.join(data2[-1]) + '\n')
    if write_toFile:
        f.close()
        f2.close()

    return data2, dict_reverse, dict_reverse_int



'''
flags =
component = !
net = @
PU =  treat it as a component only, since it's not distributed
PD =  same as above
series = %
RCM = $

flags passed into the next level
O= component
G = ground
P= pull up
B = bypass/series
S = series resistor RCM

'''
