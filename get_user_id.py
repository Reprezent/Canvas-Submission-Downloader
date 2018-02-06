#!/usr/bin/python

from __future__ import print_function


import json
import sys


if len(sys.argv) != 1:
    print(sys.stderr, "usage: python " + sys.argv[0] + " < json_request")
    sys.exit(1);

def find_user_id(json_list, assignment_string):
    for json_dict in DATA:
        try:
            if json_dict["name"] == assignment_string:
                return json_dict
        except KeyError:
            continue
    return None


decoder = json.JSONDecoder()
DATA = decoder.decode(sys.stdin.read())
course_dict = find_user_id(DATA, sys.)
    
print(course_dict["user_id"])
