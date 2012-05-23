#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Push RPMs to the local repo server
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

host="$1"
user="$2"
[ -n "$3" ] && with_python="--with-python"

cd "$(dirname "$0")/.."

echo                   "# yum -y install createrepo gcc make rpm-build rsync " \
                       "sudo wget {mysql,openssl,pcre,sqlite,zlib}-devel"
ssh      "$user@$host" mkdir -p hypernova
rsync -arvuz * "$user@$host:hypernova" \
      --exclude '.git' --exclude 'deps/python' --exclude 'install/build' \
      --exclude 'install/python'
ssh      "$user@$host" hypernova/install/rhel-build.sh $with_python
ssh      "$user@$host" rm -rf rpms/RPMS/x86_64/hypernova-*
ssh      "$user@$host" mkdir -p rpms/RPMS/x86_64
ssh      "$user@$host" cp hypernova/install/build/RPMS/x86_64/* rpms/RPMS/x86_64
ssh      "$user@$host" createrepo rpms/RPMS/x86_64/
