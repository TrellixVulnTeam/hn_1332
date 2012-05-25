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

sudo yum --assumeyes install bzip2-devel gcc {mysql,openssl,pcre,sqlite,zlib}-devel rpm-build

# Remove old artifacts
rm -rf "$instroot/build"
mkdir -p "$instroot/build/"{RPMS,SOURCES,SPECS}

if [ "$1" = "--with-python" ] || [ ! -d "$instroot/../deps/python" ]; then
    rm -rf "$instroot/python" "$instroot/deps/python"

    mkdir -p "$instroot/python"
    pushd "$instroot/python"
    wget 'http://python.org/ftp/python/3.2.3/Python-3.2.3.tar.bz2' \
         -O src.tar.bz2
    tar -xjvf src.tar.bz2
    popd

    pushd "$instroot/python/Python-3.2.3"
    ./configure \
        --prefix=/usr/local/hypernova
    make
    make install DESTDIR="$instroot/python/chroot"

    # Hack for libpython3.2m.a (see issue #321)
    chmod u+w "$instroot/python/chroot/usr/local/hypernova/lib/libpython3.2m.a"

    popd

    [ -d "$instroot/../deps/python" ] && rm -rf "$instroot/../deps/python"
    mv "$instroot/python/chroot" "$instroot/../deps/python"
fi

[ -d /tmp/hypernova ] && rm -rf /tmp/hypernova

mkdir /tmp/hypernova
pushd /tmp/hypernova

wget -c 'http://pypi.python.org/packages/source/d/distribute/distribute-0.6.24.tar.gz' -O distribute.tar.gz
tar -xzf distribute.tar.gz
mv distribute-0.6.24 python-distribute
tar -cjf "$instroot/build/SOURCES/python-distribute.tar.bz2" python-distribute
rm -rf *

cp -r "$instroot"/../{chroot,support} "$instroot/../src" .
rm -rf chroot/bin/{activate*,easy_install*,elevator,pip*,python*} \
       chroot/{include,lib*,tmp} \
       chroot/var/www/*
find 'chroot/etc' -name '*local*.ini' -type f -exec rm -f {} \;
find 'chroot/var/lib/gpg' -type f -exec rm -f {} \;
find 'chroot/var/log' -type f -exec rm -f {} \;
rm -rf src/{build,dist}

tar --exclude-vcs -cjf "$instroot/build/SOURCES/hypernova.tar.bz2" \
    chroot src support
popd

pushd "$instroot/../deps"
for dep in *
do
    tar --exclude-vcs -cjf "$instroot/build/SOURCES/$dep.tar.bz2" $dep
done
popd

rm -rf /tmp/hypernova
rpmbuild --define "_topdir $instroot/build" -ba "$instroot/rpm.spec"
