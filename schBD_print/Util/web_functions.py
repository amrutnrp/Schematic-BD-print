# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 18:24:56 2024

@author: amrutnp
"""
import os

from ansi2html import Ansi2HTMLConverter
conv = Ansi2HTMLConverter()
def make_web_page_nOpen(string_input, file_Path = 's.html', openFlag = False):

    html = conv.convert(string_input )
    html2 = html.replace ('</style>', auto_fit_css)
    f= open(file_Path, 'w', encoding= 'UTF-8')
    f.write(html2)
    f.close()

    if openFlag != False: os.startfile ( file_Path )


auto_fit_css = '''
</style>
<style>
    body {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
    }
    .content {
        font-size: 2vw; /* Adjust the value as needed */
        text-align: center;
    }
</style>
'''

