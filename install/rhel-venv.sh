#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Environment preparation
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

# Exit cleanly on error
error_trap() {
    echo " "
    echo "$0: an error occurred during the execution of an action; aborting"
    echo " "
    exit 69
}

trap error_trap 1 2 3 15 ERR

# Root of the source tree
srcroot="$(readlink -fn "$(dirname "$0")/..")"
cd $srcroot

# If forced, remove all the things
if [ "$1" == "--force" ] || [ "$2" == "--force" ]
then
    rm -rf bin/{activate*,easy_install*,pip*,python*} \
           include/ lib/ lib64
fi

# Prepare the system
#   For convenience, these can be skipped when you're running them from your
#   IDE, so you won't need to stay elevated or keep bashing out your password!
if [ "$1" != "--skip-deps" ] && [ "$2" != "--skip-deps" ]
then
    # Install system packages
    sudo yum -y install bash curl git python3

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

# Update working copy and initialise submodules (elevator, gnupg, etc.)
git pull origin master
git submodule init
git submodule update

# Set up virtualenv
pushd chroot
[ ! -f "bin/activate" ] && virtualenv --no-site-packages .
. bin/activate
popd

# Set up gnupg
pushd deps/python-gnupg
rm -rfv build/ dist/
"$srcroot/chroot/bin/python3.2" setup.py bdist_egg
"$srcroot/chroot/bin/easy_install-3.2" dist/python_gnupg-*-py3.2.egg
popd

# Install HyperNova
pushd src
rm -rfv build/ dist/
"$srcroot/chroot/bin/python3.2" setup.py bdist_egg
"$srcroot/chroot/bin/easy_install-3.2" dist/HyperNova-*-py3.2.egg
popd
