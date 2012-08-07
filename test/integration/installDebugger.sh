#!/bin/bash
# Install debugger files on a running and installed machine
#
# Copyright (c) 2012 TDM Ltd
#                    Laurent David <laurent@tdm.info>

cp -r tools/pydev/pysrc /tmp/pydev
HNPT=python3.2
HNEGGV=HyperNova-0.1.0-py3.2.egg
CURSRCPATH=$(pwd  | sed "s/\(.*\)\/test\/integration/\1/g")"/src/hypernova"

echo "Convert $CURSRCPATH into /usr/local/hypernova/lib/$HNPT/site-packages/$HNEGGV/hypernova/"

sed -i -e "s,CURRENTSOURCEPATH,$CURSRCPATH,g" -e "s,HYPERNOVAEGG,$HNEGGV,g"  -e "s,HYPERNOVAPYTHON,$HNPT,g" /tmp/pydev/pydevd_file_utils.py

echo "Copying files"
scp -P 3333 -r /tmp/pydev root@localhost:/usr/local/hypernova/lib/$HNPT/

cat << EOF
Don't forget to do the following export before running the command to debug
export PYDEVDGB_PATH=/usr/local/hypernova/lib/python3.2/pydev/
export PYDEVDGB_REMOTEIP=10.0.2.2
EOF
