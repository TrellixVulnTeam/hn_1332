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

eval set -- "$(getopt -o "bDpsv:" --long "python-binary:,python-module-st-name:,python-sitepackages-dir:,python-module-source-dir:,python-module-version:" -- "$@")"
while true; do
    case "$1" in
        -b|--python-binary            ) PYTHON_BINARY="$2"             ; shift 2 ;;
        -D|--python-module-st-name    ) PYTHON_MODULE_ST_NAME="$2"     ; shift 2 ;;
        -p|--python-sitepackages-dir  ) PYTHON_SITEPACKAGES_DIR="$2"   ; shift 2 ;;
        -s|--python-module-source-dir ) PYTHON_MODULE_SOURCE_DIR="$2"  ; shift 2 ;;
        -V|--python-module-version    ) PYTHON_MODULE_VERSION="$2"     ; shift 2 ;;
        *                             ) break                                    ;;
    esac
done

if [ ! -d "${PYTHON_SITEPACKAGES_DIR}"/${PYTHON_MODULE_ST_NAME}-${PYTHON_MODULE_VERSION}-*.egg ]; then
    pushd "${PYTHON_MODULE_SOURCE_DIR}"
    "${PYTHON_BINARY}" ./setup.py install
    popd
fi

exit 0

