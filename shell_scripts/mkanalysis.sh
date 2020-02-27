#!/bin/bash

SMOOTHING=6;
REFEVENTDUR=15;
TR=3.0;
NCONDITIONS=2;
SURFACE=fsaverage;
HEMIS=( lh rh );
PARFILE=horiwawa.par;
ANROOT="horikawa.sm";

for hemi in "${HEMIS[@]}"
do
  mkanalysis-sess \
  -fsd bold \
  -surface ${SURFACE} ${hemi} \
  -fwhm ${SMOOTHING}  \
  -event-related \
  -paradigm ${PARFILE} \
  -nconditions ${NCONDITIONS} \
  -timewindow 24 \
  -spmhrf 2 \
  -polyfit 2 \
  -mcextreg \
  -TR ${TR} \
  -refeventdur ${REFEVENTDUR} \
  -analysis ${ANROOT}${SMOOTHING}.${hemi} \
  -per-run -force
done

#repeat for MNI305 voxel-space
mkanalysis-sess \
 -fsd bold \
 -mni305 2 \
 -fwhm ${SMOOTHING} \
 -event-related \
 -paradigm ${PARFILE} \
 -nconditions ${NCONDITIONS} \
 -timewindow 24 \
 -spmhrf 2 \
 -polyfit 2 \
 -mcextreg \
 -TR ${TR} \
 -refeventdur ${REFEVENTDUR} \
 -analysis ${ANROOT}${SMOOTHING}.mni \
 -per-run -force
