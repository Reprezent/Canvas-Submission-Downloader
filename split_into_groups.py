from __future__ import print_function


import sys
import os


if len(sys.argv) != 1 and len(sys.argv) != 2:
    print(sys.stderr, "usage: python " + sys.argv[0] + "[groups_file_location]")
    sys.exit(1);

def split_into_groups(groups, student_dir="student_files"):
    # Makes the group numbers
    for i in range(len(groups)):
        if not os.path.exists(student_dir+"/"+str(i+1)):
            os.mkdir(student_dir+"/"+str(i+1))

    # Iterates over all the files in a directory
    for files in os.listdir(student_dir):
        if files.isdigit(): # Since the groups are all digits we can
            continue        # We can just check that the directory is
                            # digit.

        for i in range(len(groups)):
            name = files.split("-") # extract thier last name
            # print(groups[i][0], "<=", name[0], groups[i][0] <= name[0])
            # print(groups[i][1], ">=", name[0], groups[i][1] >= name[0])
            if  groups[i][0] <= name[0] \
            and groups[i][1] >= name[0]: # Make sure thier last name is within the group
             #   print(name[0], i + 1)
                os.rename(student_dir + "/" + files, student_dir + "/" + str(i + 1) + "/" + files) # Move the file
                break
        


def read_groups(filename):
    rv = list()
    with open(filename, "r") as group_file:
        for line in group_file:
            l = line.split("-")
            l[0] = l[0].strip()
            l[1] = l[1].strip()
            rv.append(tuple(l))

    return rv
        
groups_file = "groups"
if len(sys.argv) is 2:
    groups_file = sys.argv[1]
    # print("Groups file is {0}".format(groups_file), file=sys.stderr)



groups_list = read_groups(groups_file)
split_into_groups(groups_list)
    
