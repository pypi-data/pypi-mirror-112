# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 22:02:45 2021

@author: jianzhezhen
"""
from helloworldTZ import say_hello

def test_helloworld_no_params():
    assert say_hello() == "Hello, World!"
    
def test_helloworld_with_param():
    assert say_hello("Shiyi") == "Hello, Shiyi!"
