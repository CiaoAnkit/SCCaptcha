#!/bin/bash

cd ./test
# Command 1: Convert PNG to JPG using mogrify
find . -name "*.png" -exec sh -c 'mogrify -format jpg "$0"' {} \;

# Command 2: SCP files to remote server
scp ./13.jpg ./14.jpg ./15.jpg ./16.jpg sahithi@10.4.25.205:~/recap/deep-image-orientation-angle-detection/inputs/
