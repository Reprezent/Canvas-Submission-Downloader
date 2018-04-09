# Richard "Alex" Riedel
# Spring 2018
# This script extracts the course id number from the specified course 
# string. It is passed a json string on stdin and the course id string
# as a command line argument. It prints the couse id number to stdout

from __future__ import print_function

import json
import sys


if len(sys.argv) != 2:
    print(sys.stderr, "usage: python " + sys.argv[0] + " course-id < json-response")
    sys.exit(1)

def cache_course_codes(code_pairs):
    with open(".course_cache.txt", "w") as f:
        for k,v in enumerate(code_pairs):
            print("{0}:{1}".format(k, v), file=f)
      
def read_course_code_cache():
    rv = dict()
    try:
        with open(".course_cache.txt", "r") as f:
            for line in f:
                if not line: # If the line is not empty
                    split = line.split(":")
                    rv[split[0].strip()] = split[1].strip()
    except IOError:
        pass
    return rv

def find_course(json_list, course_string):
    for json_dict in DATA:
        try:
            if json_dict["course_code"] == course_string: # Extract the course_code from the canvas json_dictionary
                return json_dict        # Return the dictonary containing the course code.
        except KeyError:
            continue
    return None


decoder = json.JSONDecoder()
DATA = decoder.decode(sys.stdin.read()) # Decode the json from stdin.
course_dict = find_course(DATA, sys.argv[1])
    
print(course_dict["id"]) # Print the id.
