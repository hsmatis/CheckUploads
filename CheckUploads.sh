#!/bin/bash
#
# run the program which checks to see if images have been uploaded to the cloud
#
export CHECKSOURCE=/Users/family/GoogleDrive/Workspace-General/CheckUploads
cd $CHECKSOURCE/tmp
#need to go to checksource so that have persmission to write to the directory
python $CHECKSOURCE/src/CheckUploads.py > $CHECKSOURCE/CheckUploads.log # & /dev/null &
#exit
