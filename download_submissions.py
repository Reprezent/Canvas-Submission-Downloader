#!/usr/bin/python

from __future__ import print_function


import json
import sys
import os
import subprocess


try:
    from urllib.request import Request, urlopen, urlretrieve  # Python 3
except ImportError:
    from urllib2 import Request, urlopen, URLError, HTTPError # Python 2


if len(sys.argv) != 1:
    print(sys.stderr, "usage: python " + sys.argv[0] + " < json_response")
    sys.exit(1);


def get_user_name(json_resp):
    try:
        return json_resp["sortable_name"]
    except KeyError:
        return None


def get_user_name_from_id(json_dict):
    decoder = json.JSONDecoder()
    try:
        user_id = json_dict["user_id"]
        url = os.environ["HOST"] + "/" \
            + os.environ["API_VERS"] + "/" \
            + os.environ["COURSES_PATH"] + "/" \
            + os.environ["ID"] + "/" \
            + "users/" + str(user_id) + "/"

        url_req = Request(url);
        url_req.add_header("Authorization", "Bearer " + os.environ["TOKEN"])
        json_ret = urlopen(url_req).read()
        DATA = decoder.decode(json_ret)
        name = get_user_name(DATA)
        if name is not None:
            name = name.replace(", ", "-")
            name = name.replace(" ", "-")
            name = name + '-'
        #print(name, file=sys.stderr)
        return name

    except KeyError:
        return None

def find_assignments(json_list):
    rv = dict()
    for json_dict in DATA:
        try:
            name = get_user_name_from_id(json_dict)
            if name is None:
                continue
            rv[name] = list()
            for i in json_dict["attachments"]:
                try:
                    rv[name].append( (i["filename"], i["url"]) )
                except KeyError:
                    continue

        except KeyError:
            continue
    return rv

def download_all_files(files_dict): 
    directory = "student_files"
    if not os.path.exists(directory):
        os.makedirs(directory)

    for k,v in files_dict.items():
        #print(v, file=sys.stderr)
        for i in v:
            url = i[1]
            filename = directory + "/" + k+i[0]
            url_req = Request(url)
            #print(filename, file=sys.stderr)
            try:
                f = urlopen(url_req)
                with open(filename, "wb") as local_file:
                    local_file.write(f.read())
            # handle errors
            except HTTPError, e:
                print("HTTP Error:", e.code, url, file=sys.stderr)
            except URLError, e:
                print("URL Error:", e.reason, url, file=sys.stderr)


decoder = json.JSONDecoder()
course_dict = dict()
i = 1
while True:
    url = os.environ["HOST"] + "/" + os.environ["API_VERS"] + "/" + os.environ["COURSES_PATH"] + "/" \
        + os.environ["ID"] + "/" + os.environ["ASSIGNMENTS_PATH"] + "/" + os.environ["ASSIGNMENT_ID"] + "/" \
        + os.environ["SUBMISSIONS_PATH"] + "/?page=" + str(i)
    url_req = Request(url);
    url_req.add_header("Authorization", "Bearer " + os.environ["TOKEN"])
    json_ret = urlopen(url_req).read()
    DATA = decoder.decode(json_ret)
    course_dict.update(find_assignments(DATA))
    if len(DATA) == 0:
        break
    i += 1
    
download_all_files(course_dict)
