#!/usr/bin/env bash
#
# HyperNova server management framework
#
# Build the SRPM/RPMs
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

instroot="$(readlink -fn "$(dirname "$0")")"
mkdir -p "$instroot/build/SOURCES"

wget -c 'http://python.org/ftp/python/3.2.2/Python-3.2.2.tar.bz2' -O "$instroot/build/SOURCES/python.tar.bz2"

pushd /tmp
wget -c 'http://pypi.python.org/packages/source/d/distribute/distribute-0.6.24.tar.gz' -O distribute.tar.gz
tar -xzf distribute.tar.gz
mv distribute-0.6.24 python-distribute
tar -cjf "$instroot/build/SOURCES/python-distribute.tar.bz2" python-distribute
rm -rf distribute.tar.gz distribute-0.6.24
popd

pushd "$instroot/.."
tar --exclude-vcs -cjf "$instroot/build/SOURCES/hypernova.tar.bz2" src
popd

pushd "$instroot/../deps"
for dep in *
do
    tar --exclude-vcs -cjf "$instroot/build/SOURCES/$dep.tar.bz2" $dep
done
popd

rpmbuild --define "_topdir $instroot/build" -ba "$instroot/rpm.spec"
