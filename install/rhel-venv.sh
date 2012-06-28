#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Environment preparation
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

# Check whether an array contains a given value
#   $1 = arr
#   $2 = str
in_array() {
    for e in "${@:2}"; do
        [ "$e" == "$1" ] && break
    done;
}

# Exit the running script with an error status and clear warning
error_trap() {
    echo " "
    echo "$0: an error occurred during the execution of an action; aborting" >&2
    echo " "
    exit 69
}

# Bail out now unless the user is in a virtualenv context -- we'll probably
# modify global system configuration!
[ -z "$VIRTUAL_ENV" ] && echo "$0: activate a virtualenv first!" >&2 \
                      && exit
# Establish what we need to do before initiating error trapping, since we have
# to return error exit statuses in in_array
FORCE=0
in_array '--force' "${@}"
[ "$?" == 0 ] && FORCE=1

SKIPDEPS=0
in_array '--skip-deps' "${@}"
[ "$?" == 0 ] && SKIPDEPS=1

# Don't risk screwing the system up; exit early
trap error_trap 1 2 3 15 ERR

# Root of the source tree
srcroot="$(readlink -fn "$(dirname "$0")/..")"
cd $srcroot

# If forced, remove all the things
if [ "$FORCE" == 1 ]
then
    rm -rf $srcroot/chroot/bin/{activate*,easy_install*,pip*,py*}
fi

# Prepare the system
#   For convenience, these can be skipped when you're running them from your
#   IDE, so you won't need to stay elevated or keep bashing out your password!
if [ "$SKIPDEPS" != 1 ]; then
    # Install system packages
    sudo yum -y install bash curl git python3{,-devel,-libs}

    # Set up setuptools/distribute
    pushd /tmp
    sudo python3.2 < <(curl -s http://python-distribute.org/distribute_setup.py)
    rm -f distribute_setup.py
    popd

    # Set up virtualenv
    sudo easy_install-3.2 virtualenv

    # Set up elevator
    pushd deps/elevator
    info=( $(grep -P "^$USER:" /etc/passwd | sed 's/:/ /g' | awk '{print $3, $4}') )
    ./configure --prefix=../../chroot \
                --allow-uid="${info[0]}" \
                --allow-gid="${info[1]}" \
                --target-uid=0 \
                --target-gid=0
    make
    sudo make install
    popd
fi

# Set up virtualenv
if [ "$FORCE" == 1 ] || [ -f bin/activate ]; then
    pushd chroot
    [ ! -f "bin/activate" ] && virtualenv --no-site-packages .
    . bin/activate
    popd

    # Patch virtualenv activation file
    echo "
    export BINDIR="$srcroot/chroot/bin"
    export CONFDIR="$srcroot/chroot/etc/hypernova"
    " >> "$srcroot/chroot/bin/activate"
fi

# Install Python dependencies
if [ "$SKIPDEPS" != 1 ]; then
    # Set up pexpect
    pushd deps/python-pexpect
    rm -rfv build/ dist/
    "$srcroot/chroot/bin/python3.2" setup.py bdist_egg
    "$srcroot/chroot/bin/easy_install-3.2" dist/pexpect-*-py3.2.egg
    popd

    # Set up gnupg
    pushd deps/python-gnupg
    rm -rfv build/ dist/
    "$srcroot/chroot/bin/python3.2" setup.py bdist_egg
    "$srcroot/chroot/bin/easy_install-3.2" dist/python_gnupg-*-py3.2.egg
    popd

    # Set up oursql
    pushd deps/python-oursql
    rm -rfv build/ dist/
    "$srcroot/chroot/bin/python3.2" setup.py bdist_egg
    "$srcroot/chroot/bin/easy_install-3.2" dist/oursql-*-py3.2-linux-$(arch).egg
    popd

    # Set up pyrg
    pushd deps/python-pyrg
    rm -rfv build/ dist/
    "$srcroot/chroot/bin/python3.2" setup.py bdist_egg
    "$srcroot/chroot/bin/easy_install-3.2" dist/pyrg-*-py3.2.egg
    popd
fi

# Install HyperNova
pushd src
rm -rfv build/ dist/
"$srcroot/chroot/bin/python3.2" setup.py bdist_egg
"$srcroot/chroot/bin/easy_install-3.2" dist/HyperNova-*-py3.2.egg
popd
