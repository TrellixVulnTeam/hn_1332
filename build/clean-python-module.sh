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

eval set -- "$(getopt -o "dlnr:" --long "python-module-source-dir:,is-local-submodule,python-module-name:,rpm-output-dir:" -- "$@")"
while true; do
    case "$1" in
        -d|--python-module-source-dir) PYTHON_MODULE_SOURCE_DIR="$2" ; shift 2 ;;
        -l|--is-local-submodule      ) KEEP_SOURCE_DIR=1             ; shift 1 ;;
        -n|--python-module-name      ) PYTHON_MODULE_NAME="$2"       ; shift 2 ;;
        -r|--rpm-output-dir          ) RPM_OUTPUT_DIR="$2"           ; shift 2 ;;
        *                            ) break                                   ;;
    esac
done

if [ "${KEEP_SOURCE_DIR}" = "1" ]; then
    rm -rfv "${PYTHON_MODULE_SOURCE_DIR}"/{build,dist}
else
    rm -rfv "${PYTHON_MODULE_SOURCE_DIR}"
fi

rm -fv "${RPM_OUTPUT_DIR}"/*/hypernova-python-${PYTHON_MODULE_NAME}-*

exit 0

