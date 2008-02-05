#!/bin/bash
#
# example test runner shell script
#

# full path to the python interpretor
export PYTHON="/home/piv/python-2.4.3/bin/python"

# path to ZOPE_HOME/lib/python
export SOFTWARE_HOME="/data/piv/work/zope-2.9.5/lib/python"


# path to your instance. Don't set it if you aren't having  instance
export INSTANCE_HOME="/home/piv/zinstances/something/"

${PYTHON} runalltests.py
