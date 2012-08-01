#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Elevator install script
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

cd "$(dirname "$(readlink -fn "$0")")"
. core.sh

trap error_trap 1 2 3 15 ERR

eval set -- "$(getopt -o "bsv:" --long "elevator-binary:,elevator-source-dir:,elevator-venv-prefix:" -- "$@")"
while true; do
    case "$1" in
        -b|--elevator-binary     ) ELEVATOR_BINARY="$2"      ; shift 2 ;;
        -s|--elevator-source-dir ) ELEVATOR_SOURCE_DIR="$2"  ; shift 2 ;;
        -v|--elevator-venv-prefix) ELEVATOR_VENV_PREFIX="$2" ; shift 2 ;;
        *                        ) break                               ;;
    esac
done

if [ ! -x "${ELEVATOR_BINARY}" ]; then
    cp "${ELEVATOR_SOURCE_DIR}/build/elevator" "${ELEVATOR_VENV_PREFIX}/bin"
fi

exit 0

