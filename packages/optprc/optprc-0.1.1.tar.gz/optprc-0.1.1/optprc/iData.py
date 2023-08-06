# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 10:28:06 2021

@author: gyg
"""

import json


def save_json(dicts, filepath):
    with open(filepath, 'w') as result_file:
        json.dump(dicts, result_file)
        
        return True

def read_json(filepath):
    with open(filepath, 'r') as result_file:
        return json.load(result_file)