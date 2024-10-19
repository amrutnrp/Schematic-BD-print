

compact_flag = False


series_block = " ┌{}┐ \n─┤{}├─\n └{}┘ "
# series_block = "─<{}>─"


def box_series(text):
    if compact_flag: return box_series_v2(text)
    """
                       ┌─────┐
    Convertes C49 --> ─┤ C49 ├─
                       └─────┘
    """
    width = '─' * (len(text) + 2 )
    middle = f" {text} "
    return series_block.format( width, middle, width)
    # return series_block.format( middle)



# Comp_open_block_r = " {} ├─"
# Comp_open_block_l = "─┤ {} "

Comp_open_block_r = " {} ╟─"
Comp_open_block_l = "─╢ {} "

# Comp_open_block_r = " {} ]─"
# Comp_open_block_l = "─[ {} "


def box_comp_open(text, dirn = True):

    """
    dirn can be "l" or "r"
    U48, True --> ─┤ U48
    U48, False -->  U48 ├─
    """

    if not compact_flag : return box_comp_open_v2(text, dirn )

    if dirn == True:
        local_block = Comp_open_block_l
    else:
        local_block = Comp_open_block_r
    return local_block.format( text)


Comp_gnd_block = " {}┴{} \n {} \n╘{}═{}╛"

def box_comp_PD(text):
    """
               ──┴──
    C1202-->   C1202
              ╘═════╛
    """
    if compact_flag : return box_comp_PD_v2(text)
    if len(text)%2 == 0:
        text2 = text+' '
    else:
        text2 = text
    width = len(text2) >> 1
    mid1 = '─'* width
    mid2 = '═'* width
    return Comp_gnd_block  .format (mid1,mid1, text2, mid2, mid2)


pull_up_chr = chr(0x21EF)


def box_pullup(text_net, text_res, dirn = True):
    """
    dirn : True for left, False for right
    Convertes
    1P8 , R123, True -->  ─R123 ⇯ 1P8
    1P8 , R123, False -->  1P8 ⇯ R123─

    """
    if dirn== True:
        return '─{} {} {}'.format (text_res, pull_up_chr, text_net)
    else:
        return '{} {} {}─'.format (text_net, pull_up_chr, text_res)


# Compv2_open_block_r = "┌{}┐ \n│ {} ├─\n└{}┘ "
# Compv2_open_block_l = " ┌{}┐\n─┤ {} │\n └{}┘"

Compv2_open_block_r = "╔{}╗ \n║ {} ╟─\n╚{}╝ "
Compv2_open_block_l = " ╔{}╗\n─╢ {} ║\n ╚{}╝"


def box_comp_open_v2(text, dirn = True):
    """
    dirn can be "l" or "r"
    U48, True --> ─┤ U48
    U48, False -->  U48 ├─
    """
    width = '═' * (len(text) + 2 )
    if dirn == True:
        local_block = Compv2_open_block_l
    else:
        local_block = Compv2_open_block_r
    return local_block.format( width, text, width)


series_block_v2 = "─<{}>─"


def box_series_v2(text):
    """
                       ┌─────┐
    Convertes C49 --> ─┤ C49 ├─
                       └─────┘
    """
    width = '─' * (len(text) + 2 )
    middle = f" {text} "
    return series_block_v2.format( middle)

Comp_gnd_block_v2 = " {}┴{} \n {} "
def box_comp_PD_v2(text):
    """
               ──┴──
    C1202-->   C1202
    """

    if len(text)%2 == 0:
        text2 = text+' '
    else:
        text2 = text
    width = len(text2) >> 1
    mid1 = '─'* width
    # mid2 = '═'* width
    return Comp_gnd_block_v2  .format (mid1,mid1, text2)


Compv3_open_block_r = "╔{}╧{}╗\n║ {} ║\n╚{}╝"

def box_comp_open_v3_top(text, *other):
    """
    dirn can be "l" or "r"
    U48, True --> ─┤ U48
    U48, False -->  U48 ├─
    """
    width = '═' * (len(text) + 2 )
    width2 = len(text) >> 1

    if len(text)%2 == 0:
        wd31 = '═' * (width2 )
        wd32 = '═' * ((width2 )+ 1 )

    else:
        wd31 = wd32 = '═' * ( width2  + 1 )

    return Compv3_open_block_r.format( wd31,wd32, text, width)

