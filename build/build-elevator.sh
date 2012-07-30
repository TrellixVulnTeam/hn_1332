#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Makefile wrapper for build actions
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

cd "$(dirname "$(readlink -fn "$0")")"
. core.sh

trap error_trap 1 2 3 15 ERR

eval set -- "$(getopt -o "d:" --long "elevator-source-dir:" -- "$@")"
while true; do
    case "$1" in
        -d|--elevator-source-dir) ELEVATOR_SOURCE_DIR="$2" ; shift 2 ;;
        *                       ) break                              ;;
    esac
done

if [ ! -f "${ELEVATOR_SOURCE_DIR}/.hypernova_build_complete" ]; then
    pushd "${ELEVATOR_SOURCE_DIR}"
    pwd
    ./configure --prefix=
    make
    touch ".hypernova_build_complete"
    popd
fi

exit 0

