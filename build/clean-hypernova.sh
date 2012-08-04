#!/usr/bin/env bash

#
# HyperNova server management framework
#
# HyperNova clean script
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

cd "$(dirname "$(readlink -fn "$0")")"
. core.sh

trap error_trap 1 2 3 15 ERR

eval set -- "$(getopt -o "dlr:" --long "hypernova-source-dir:,rpm-output-dir:" -- "$@")"
while true; do
    case "$1" in
        -d|--hypernova-source-dir) HYPERNOVA_SOURCE_DIR="$2" ; shift 2 ;;
        -r|--rpm-output-dir      ) RPM_OUTPUT_DIR="$2"       ; shift 2 ;;
        *                        ) break                               ;;
    esac
done

rm -rfv "${HYPERNOVA_SOURCE_DIR}"/{build,dist}
rm -fv "${RPM_OUTPUT_DIR}"/*/hypernova-core-*

exit 0

