#!/bin/bash

SUBJECT=1
TEST=1
RUN=1

while [ $SUBJECT -le 5 ]
do
    DIR="sub-0$SUBJECT/ses-perceptionTest0$TEST/func"
    if [ -d $DIR ]; then
        echo "$DIR/*.nii.gz bold/$RUN/f.nii.gz"
        (( RUN++ ))
    fi
done
