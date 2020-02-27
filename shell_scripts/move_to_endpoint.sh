#!/bin/bash

subject=1

while [ $subject -le 5 ]
do
    scp -r tsv_out/FS_0$subject/bold/* avery@128.205.172.41:horikawa/FS_0$subject/bold
    (( subject++ ))
done
