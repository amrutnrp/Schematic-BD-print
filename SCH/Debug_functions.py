# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 01:29:16 2024

@author: amrutnp
"""

def view_str(string):
    print ( '\n' .join (string ) )


def validate_rect(string):
    if type(string) == str:
        str2 = string.split('\n')
        len_I = [   len(i) for i in str2]
    elif type(string) == list:
        len_I = [   len(i) for i in string]
    else:
        print ('FATAL error in rectangle check ')
    len_all = set (len_I )
    return True if len(len_all) == 1 else False

def shape(string):
    return len(string), len(string [0])
