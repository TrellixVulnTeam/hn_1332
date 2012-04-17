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

cd "$(dirname "$0")/.."
rm -rf install/build

echo                   "sudo yum -y install createrepo gcc make rpm-build wget" \
                       {mysql,openssl,pcre,sqlite,zlib}-devel
ssh      "$user@$host" rm -rf hypernova
ssh      "$user@$host" mkdir -p hypernova
scp -r * "$user@$host:hypernova"
ssh      "$user@$host" hypernova/install/rhel-build.sh
ssh      "$user@$host" rm -rf rpms/RPMS/x86_64/hypernova-*
ssh      "$user@$host" mkdir -p rpms/RPMS/x86_64
ssh      "$user@$host" cp hypernova/install/build/RPMS/x86_64/* rpms/RPMS/x86_64
ssh      "$user@$host" createrepo rpms/RPMS/x86_64/
