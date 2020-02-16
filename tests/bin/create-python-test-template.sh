#!/bin/bash
#
# This script will attempt to find all methods and functions in a $ARGV1 file
# and output the test results to STDIO.
#
# It is helpful in getting things started.
#
grep 'def ' $1 | awk '{print $2}' | awk -F\( '{print "    def test_" $1 "(self):\n        \"\"\"Testing method or function named \"" $1 "\".\"\"\"\n        pass\n"}'
