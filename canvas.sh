#!/usr/bin/sh
# Richard "Alex" Riedel
# Spring 2018
# This script pulls all submissions for a particular assignment
# on canvas, with thier specified names. 
# This script requires 

# Gets the name of the assignment from the cmd line arguments.
ASSIGNMENT=$1
export HOST="https://utk.instructure.com"
export API_VERS="api/v1"
export COURSES_PATH="courses"
export ASSIGNMENTS_PATH="assignments"
export SUBMISSIONS_PATH="submissions"
COURSE_CODE="COSC302"
# Absolute path to this script, e.g. /home/user/bin/foo.sh
SCRIPT=$(readlink -f "$0")
# Absolute path this script is in, thus /home/user/bin
SCRIPT_PATH=$(dirname "$SCRIPT")




if [ "$#" -ne 1 ]; then
    echo "Usage: $0 Lab-Name" >&2
    exit 1
fi

if [ ! -f "$SCRIPT_PATH/token" ]; then
    printf "token needed for use with Canvas API\nAdd a token to this path $SCRIPT_PATH\n";
    exit 2
fi

if [ ! -f "$SCRIPT_PATH/groups" ]; then
    printf "groups file needed for use with splitting the group\nAdd a file with student groups to this path $SCRIPT_PATH\n";
    exit 2
fi
export TOKEN=$(<$SCRIPT_PATH/token)

# Requests courses for user.
COURSES_REQUEST=$(curl $HOST/$API_VERS/$COURSES_PATH/ \
                   -H "Authorization: Bearer "$TOKEN \
                   2> /dev/null)
RV=$?
if [ ! $RV ]; then
    printf "Course request failed.\nExiting....\n"
    exit $RV
fi

# Extracts the Course ID from the course code.
ID=$(python $SCRIPT_PATH/extract_course_id.py $COURSE_CODE <<< """$COURSES_REQUEST""")

RV=$?
if [ "$RV" != "0" ]; then
    printf "Extracting Course ID Failed.\nExiting....\n"
    exit $RV
fi

export ID


# Gets a json request of all assignments offered on a course. (This needs to be pagenated)
ASSIGNMENTS_REQUEST=$(curl $HOST/$API_VERS/$COURSES_PATH/$ID/$ASSIGNMENTS_PATH/ \
                       -X "GET" \
                       -H "Authorization: Bearer "$TOKEN \
                       2> /dev/null)

RV=$?
if [ "$RV" != "0" ]; then
    printf "Assignment Request Failed.\nExiting....\n"
    exit $RV
fi

# Extracts the assignment id number from the assignment string passed
ASSIGNMENT_ID=$(python $SCRIPT_PATH/extract_assignment_id.py "$ASSIGNMENT" <<< """$ASSIGNMENTS_REQUEST""")

RV=$?
if [ "$RV" != "0" ]; then
    printf "Assignment ID Extraction Failed.\nExiting....\n"
    exit $RV
fi

export ASSIGNMENT_ID
# Downloads all the submissions of the specified ASSIGNMENT_ID environment variable.
DOWNLOAD_LINKS=$(python $SCRIPT_PATH/download_submissions.py $SCRIPT_PATH/.name-id-cache)

RV=$?
if [ "$RV" != "0" ]; then
    printf "Downloading Submissions Failed.\nExiting....\n"
    exit $RV
fi

(python $SCRIPT_PATH/split_into_groups.py $SCRIPT_PATH/groups)

RV=$?
if [ "$RV" != "0" ]; then
    printf "Splitting into Groups Failed.\nExiting....\n"
    exit $RV
fi
