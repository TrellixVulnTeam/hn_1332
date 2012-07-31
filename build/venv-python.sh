#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Python install script
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

cd "$(dirname "$(readlink -fn "$0")")"
. core.sh

trap error_trap 1 2 3 15 ERR

eval set -- "$(getopt -o "sv:" --long "python-source-dir:,python-venv-prefix:" -- "$@")"
while true; do
    case "$1" in
        -s|--python-source-dir ) PYTHON_SOURCE_DIR="$2"  ; shift 2 ;;
        -v|--python-venv-prefix) PYTHON_VENV_PREFIX="$2" ; shift 2 ;;
        *                      ) break                             ;;
    esac
done

if [ ! -x "${PYTHON_VENV_PREFIX}/bin"/python* ]; then
    pushd "${PYTHON_SOURCE_DIR}"
    DESTDIR="${PYTHON_VENV_PREFIX}" make install
    popd
fi

exit 0

