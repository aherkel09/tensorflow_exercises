#!/bin/bash

SUBJECT=1
COUNTER=1
COUNTER_ZEROS="00"

while [ $SUBJECT -le 5 ]; do
  RUN=1

  mkdir FS_0$SUBJECT
  mkdir FS_0$SUBJECT/bold

  while [ $RUN -le 35 ]; do
    if [ $COUNTER -ge 100 ]; then
      COUNTER_ZEROS=""
    elif [ $COUNTER -ge 10 ]; then
      COUNTER_ZEROS="0"
    fi

    ZEROS="00"

    if [ $RUN -ge 100 ]; then
      ZEROS=""
    elif [ $RUN -ge 10 ]; then
      ZEROS="0"
    fi

    mkdir FS_0$SUBJECT/bold/$ZEROS$RUN
    cp horikawa$COUNTER_ZEROS$COUNTER.par FS_0$SUBJECT/bold/$ZEROS$RUN/horikawa.par

    (( RUN++ ))
    (( COUNTER++ ))
  done

  (( SUBJECT++ ))
done
