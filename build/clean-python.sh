#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Python build script
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

cd "$(dirname "$(readlink -fn "$0")")"
. core.sh

trap error_trap 1 2 3 15 ERR

eval set -- "$(getopt -o "d:" --long "python-source-dir:" -- "$@")"
while true; do
    case "$1" in
        -d|--python-source-dir) PYTHON_SOURCE_DIR="$2"  ; shift 2 ;;
        *                     ) break                             ;;
    esac
done

rm -rfv "${PYTHON_SOURCE_DIR}"

exit 0
