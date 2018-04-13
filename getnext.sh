#!/usr/bin/sh

search_dir="student_files/2"
copy_dir="temp/"
used_file=".last_used"
found=0


if [ -f "$used_file" ]; then
    LAST_USED=$(cat $used_file)
fi

for entry in "$search_dir"/*; do
    # echo $entry $LAST_USED
    if [ ! -f "$used_file" ]; then
        echo $entry > "$used_file"
        printf "Copying $entry to $copy_dir$(basename -- "$entry")\n"
        cp $entry $copy_dir$(basename -- "$entry")
        exit 0
    fi

    if [ $found -eq 1 ]; then
        echo $entry > "$used_file"
        printf "Copying $entry to $copy_dir$(basename -- "$entry")\n"
        cp $entry $copy_dir$(basename -- "$entry")
        exit 0
    fi

    if [ "$LAST_USED" == "$entry" ]; then
        found=1
    fi

done


printf "No more files to copy.\n"
rm $used_file
