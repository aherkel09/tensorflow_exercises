#!/bin/bash

SUBJECT=1
TEST=1
RUN=1
FILES=""

while [ $SUBJECT -le 5 ]
do
    DIR="sub-0$SUBJECT/ses-perceptionTest0$TEST/func"
    if [ -d $DIR ]; then
        FILES=$DIR/*.nii.gz
    fi

    echo "$FILES"

    for f in $FILES
    do
        echo "$f"
    done
done
