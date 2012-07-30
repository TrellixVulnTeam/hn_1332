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

eval set -- "$(getopt -o "dr:" --long "elevator-source-dir:,rpm-output-dir:" -- "$@")"
while true; do
    case "$1" in
        -d|--elevator-source-dir) ELEVATOR_SOURCE_DIR="$2" ; shift 2 ;;
        -r|--rpm-output-dir     ) RPM_OUTPUT_DIR="$2"      ; shift 2 ;;
        *                       ) break                              ;;
    esac
done

pushd "${ELEVATOR_SOURCE_DIR}"
make clean
rm -f ".hypernova_build_complete"
popd

rm -fv  "${RPM_OUTPUT_DIR}"/*/hypernova-elevator

exit 0

