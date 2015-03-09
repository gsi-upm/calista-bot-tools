#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "usage: testAll.sh BOTURL"
    exit 1
fi 

TESTCONTROLLER=test_fe_controller.py
TMPDIR=`mktemp -d`

# Test without strict mode first
./$TESTCONTROLLER -u $1 -o $TMPDIR/testNormal.log

# Test with strict mode
./$TESTCONTROLLER -u $1 -s -o $TMPDIR/testStrict.log

# Give the results
NORMAL=`tail -n 1 $TMPDIR/testNormal.log`
STRICT=`tail -n 1 $TMPDIR/testStrict.log`
echo "Normal results: $NORMAL" 
echo "Strict results: $STRICT" 

# Clear all
rm -r $TMPDIR