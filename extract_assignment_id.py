from __future__ import print_function


import json
import sys


if len(sys.argv) != 2:
    print(sys.stderr, "usage: python " + sys.argv[0] + " assignment-name < json-response")
    sys.exit(1);

def find_assignment(json_list, assignment_string):
    for json_dict in DATA:
        try:
            if json_dict["name"] == assignment_string:
                return json_dict
        except KeyError:
            continue
    return None


decoder = json.JSONDecoder()
DATA = decoder.decode(sys.stdin.read())
course_dict = find_assignment(DATA, sys.argv[1])
    
print(course_dict["id"])
