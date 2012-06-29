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
#   $1 = str
#   $2 = arr
in_array() {
    for e in "${@:2}"; do
        [ "$e" == "$1" ] && return 0
    done;

    return 1
}

# Exit the running script with an error status and clear warning
error_trap() {
    if [ "$EXIT_ON_ERROR" = "1" ]; then
        echo " "
        echo "$0: an error occurred during the execution of an action; aborting" >&2
        echo " "
        exit 69
    else
        echo "$0: being tolerant of possible error condition" >&2
    fi
}

# Enable error trapping (die on error)
trap_on() {
    EXIT_ON_ERROR=1
}

# Disable error trapping
trap_off() {
    EXIT_ON_ERROR=0
}

# Establish what we need to do before initiating error trapping, since we have
# to return error exit statuses in in_array
FORCE=0
in_array '--force' "${@}"
[ "$?" == 0 ] && FORCE=1

SKIPDEPS=0
in_array '--skip-deps' "${@}"
[ "$?" == 0 ] && SKIPDEPS=1

# Bail out now unless the user is in a virtualenv context -- we'll probably
# modify global system configuration!
if [ -z "$VIRTUAL_ENV" ] && [ $FORCE -eq 0 ]; then
    echo "$0: activate a virtualenv first!" >&2 \
    echo "If this is your first time, use the --force to install a fresh one"
    exit
fi

# Don't risk screwing the system up; exit early
trap_on

# Root of the source tree
srcroot="$(readlink -fn "$(dirname "$0")/..")"
cd $srcroot

# If forced, remove all the things
if [ "$FORCE" == 1 ]
then
    rm -rf $srcroot/chroot/bin/{activate,easy_install,pip,py}*
    pythonbrew venv delete hypernova
fi

# Prepare the system
#   For convenience, these can be skipped when you're running them from your
#   IDE, so you won't need to stay elevated or keep bashing out your password!
if [ "$SKIPDEPS" = 0 ]; then
    # Install system packages
    sudo yum -y install bash curl git

    # Disable error trapping while we process options
    trap_off

    # Bail if Python 3.2 isn't available on $PATH
    which python3.2 >/dev/null
    retval="$?"
    if [ "$?" != "0" ]; then
        echo "python3.2 must be available on your PATH!"
        exit 1
    fi

    # Detect pythonbrew; we can sidestep the system python totally then
    USE_PYTHONBREW=0
    in_array "--use-pythonbrew" "${@}"
    retval="$?"
    if [ "$retval" = 0 ] || [[ "$PYTHONPATH" =~ "$HOME/.pythonbrew" ]]; then
        echo "pythonbrew detected or forced; we'll assume a per-user install"
        USE_PYTHONBREW=1
    fi

    # Re-enable error trapping
    trap_on

    # Set up setuptools/distribute and virtualenv
    if [ "$USE_PYTHONBREW" = 0 ]; then
        pushd /tmp
        sudo python3.2 < <(curl -s http://python-distribute.org/distribute_setup.py)
        rm -f distribute_setup.py
        popd

        sudo easy_install-3.2 virtualenv
    else
        pythonbrew switch 3.2.3
        pythonbrew venv init
        pythonbrew venv create hypernova
        pythonbrew venv use hypernova
    fi

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
if [ "$FORCE" == 1 ] || [ ! -f bin/activate ]; then
    if [ "$USE_PYTHONBREW" = "0" ]; then
        pushd chroot
        if [ ! -f "bin/activate" ]; then
            virtualenv --help
            virtualenv "$(pwd)"
        fi
        . bin/activate
        popd
    else
        touch "$srcroot/chroot/bin/activate"
        ln -s "$(which python3.2)" "$srcroot/chroot/bin/python3.2"
    fi

    # Patch virtualenv activation file
    echo "
    export BINDIR="$srcroot/chroot/bin"
    export CONFDIR="$srcroot/chroot/etc/hypernova"
    export PATH="\$PATH:\$BINDIR"
    " >> "$srcroot/chroot/bin/activate"
fi

# Install Python dependencies
if [ "$SKIPDEPS" != 1 ]; then
    # Set up pexpect
    pushd deps/python-pexpect
    rm -rfv build/ dist/
    "python3.2" setup.py bdist_egg
    "easy_install-3.2" dist/pexpect-*-py3.2.egg
    popd

    # Set up gnupg
    pushd deps/python-gnupg
    rm -rfv build/ dist/
    "python3.2" setup.py bdist_egg
    "easy_install-3.2" dist/python_gnupg-*-py3.2.egg
    popd

    # Set up oursql
    pushd deps/python-oursql
    rm -rfv build/ dist/
    "python3.2" setup.py bdist_egg
    "easy_install-3.2" dist/oursql-*-py3.2-linux-$(arch).egg
    popd

    # Set up pyrg
    pushd deps/python-pyrg
    rm -rfv build/ dist/
    "python3.2" setup.py bdist_egg
    "easy_install-3.2" dist/pyrg-*-py3.2.egg
    popd
fi

# Install HyperNova
pushd src
rm -rfv build/ dist/
"python3.2" setup.py bdist_egg
"easy_install-3.2" dist/HyperNova-*-py3.2.egg
popd
