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

eval set -- "$(getopt -o "di:" --long "python-source-dir:,python-install-dir:" -- "$@")"
while true; do
    case "$1" in
        -d|--python-source-dir ) PYTHON_SOURCE_DIR="$2"  ; shift 2 ;;
        -i|--python-install-dir) PYTHON_INSTALL_DIR="$2" ; shift 2 ;;
        *                      ) break                             ;;
    esac
done

pushd "${PYTHON_SOURCE_DIR}"
DESTDIR="${PYTHON_INSTALL_DIR}" make install

exit 0
