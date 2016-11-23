import sys
import json

def load_conf(filename) :
    with open(filename, "r") as in_file :
        data = json.load(in_file)
    return data
