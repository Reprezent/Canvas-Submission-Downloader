
from __future__ import print_function


import json
import sys
import os
import subprocess
import asyncio


try:
    from urllib.request import Request, urlopen, urlretrieve  # Python 3
except ImportError:
    from urllib2 import Request, urlopen, URLError, HTTPError # Python 2


if len(sys.argv) != 1 and len(sys.argv) != 2:
    print("usage: python " + sys.argv[0] + " [cache location]", file=sys.stderr)
    sys.exit(1);

global_name_cache = None
CACHE_FILE_NAME = ".name-id-cache"
if len(sys.argv) == 2:
    CACHE_FILE_NAME = sys.argv[1]

def read_cache(filename=".name-id-cache"):
    # Caches the id -> name field.
    name_cache = dict()
    try:
        with open(filename, "r") as f:
            for line in f:
                kv = line.strip().split(":")
                kv[0] = int(kv[0])
                # print("READ CACHE: Added {0} = {1} to cache, thier types are {2}, {3}".format(kv[0], kv[1], type(kv[0]), type(kv[1])), file=sys.stderr)
                name_cache[kv[0]] = kv[1]
    except IOError:
        pass
    return name_cache
        
    

def get_user_name(json_resp):
    try:
        return json_resp["sortable_name"]
    except KeyError:
        return None


def get_user_name_from_id(json_dict):
    decoder = json.JSONDecoder()
    try:
        user_id = json_dict["user_id"]
        if user_id in global_name_cache:
            return global_name_cache[user_id]

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
            name = str(name)
            # print(str(user_id) + ": " + name, file=sys.stderr)
            # print("GET ID: Added {0} = {1} to cache, thier types are {2}, {3}".format(user_id, name, type(user_id), type(name)), file=sys.stderr)
            global_name_cache[user_id] = name
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


def write_cache(cache, filename=".name-id-cache"):
    with open(filename, "w") as f:
        for k,v in cache.items():
            # print("Wririntg {0}:{1} to cache".format(k, v), file=sys.stderr)
            print("{0}:{1}".format(k, v), file=f)

decoder = json.JSONDecoder()
course_dict = dict()
global_name_cache = read_cache(CACHE_FILE_NAME)
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
write_cache(global_name_cache, CACHE_FILE_NAME)
