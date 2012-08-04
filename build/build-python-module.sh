#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Python module build tool
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

cd "$(dirname "$(readlink -fn "$0")")"
. core.sh

trap error_trap 1 2 3 15 ERR

eval set -- "$(getopt -o "dDnptu:" --long "python-module-source-dir:,just-download,python-module-name:,python-binary:,python-module-version:,build-temp-dir:,python-module-source-url:" -- "$@")"
while true; do
    case "$1" in
        -d|--python-module-source-dir) PYTHON_MODULE_SOURCE_DIR="$2" ; shift 2 ;;
        -D|--just-download           ) JUST_DOWNLOAD="1"             ; shift 1 ;;
        -n|--python-module-name      ) PYTHON_MODULE_NAME="$2"       ; shift 2 ;;
        -p|--python-binary           ) PYTHON_BINARY="$2"            ; shift 2 ;;
        -t|--build-temp-dir          ) BUILD_TEMP_DIR="$2"           ; shift 2 ;;
        -u|--python-module-source-url) PYTHON_MODULE_SOURCE_URL="$2" ; shift 2 ;;
        *                            ) break                                   ;;
    esac
done

if [ ! -d "${PYTHON_MODULE_SOURCE_DIR}" ] && [ -n "${PYTHON_MODULE_SOURCE_URL}" ]; then
    mkdir -p "${PYTHON_MODULE_SOURCE_DIR}"
    wget -O "${BUILD_TEMP_DIR}/python-${PYTHON_MODULE_NAME}.tar.gz" "${PYTHON_MODULE_SOURCE_URL}"
    tar -xzvf "${BUILD_TEMP_DIR}/python-${PYTHON_MODULE_NAME}.tar.gz" -C "${BUILD_TEMP_DIR}"
    mv "${BUILD_TEMP_DIR}"/${PYTHON_MODULE_NAME}-*/* "${PYTHON_MODULE_SOURCE_DIR}"
fi

[ "${JUST_DOWNLOAD}" = "1" ] && exit 0

if [ ! -f "${PYTHON_MODULE_SOURCE_DIR}/.hypernova_build_complete" ]; then
    pushd "${PYTHON_MODULE_SOURCE_DIR}"
    "${PYTHON_BINARY}" ./setup.py bdist_egg
    touch ".hypernova_build_complete"
    popd
fi

exit 0

