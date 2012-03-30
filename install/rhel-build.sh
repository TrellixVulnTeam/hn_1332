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

wget 'http://python.org/ftp/python/3.2.2/Python-3.2.2.tar.bz2' \
     -O "$instroot/build/SOURCES/python.tar.bz2"

[ -d /tmp/hypernova ] && rm -rf /tmp/hypernova

mkdir /tmp/hypernova
pushd /tmp/hypernova

wget -c 'http://pypi.python.org/packages/source/d/distribute/distribute-0.6.24.tar.gz' -O distribute.tar.gz
tar -xzf distribute.tar.gz
mv distribute-0.6.24 python-distribute
tar -cjf "$instroot/build/SOURCES/python-distribute.tar.bz2" python-distribute
rm -rf *

cp -r "$instroot/../chroot" "$instroot/../src" .
rm -rf chroot/bin/{activate*,easy_install*,elevator,pip*,python*} \
       chroot/{include,lib*,tmp}
find 'chroot/etc' -name '*local*.ini' -type f -exec rm -f {} \;
find 'chroot/var/lib/hypernova/gpg' -type f -exec rm -f {} \;
find 'chroot/var/log' -type f -exec rm -f {} \;

tar --exclude-vcs -cjf "$instroot/build/SOURCES/hypernova.tar.bz2" \
    chroot src
popd

pushd "$instroot/../deps"
for dep in *
do
    tar --exclude-vcs -cjf "$instroot/build/SOURCES/$dep.tar.bz2" $dep
done
popd

rm -rf /tmp/hypernova
rpmbuild --define "_topdir $instroot/build" -ba "$instroot/rpm.spec"
