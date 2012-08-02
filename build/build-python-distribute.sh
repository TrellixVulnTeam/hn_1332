#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Python Distribute build tool
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

cd "$(dirname "$(readlink -fn "$0")")"
. core.sh

trap error_trap 1 2 3 15 ERR

eval set -- "$(getopt -o "dptu:" --long "python-distribute-source-dir:,python-binary:,python-distribute-version:,build-temp-dir:,python-distribute-source-url:" -- "$@")"
while true; do
    case "$1" in
        -d|--python-distribute-source-dir) PYTHON_DISTRIBUTE_SOURCE_DIR="$2" ; shift 2 ;;
        -p|--python-binary               ) PYTHON_BINARY="$2"                ; shift 2 ;;
        -t|--build-temp-dir              ) BUILD_TEMP_DIR="$2"               ; shift 2 ;;
        -u|--python-distribute-source-url) PYTHON_DISTRIBUTE_SOURCE_URL="$2" ; shift 2 ;;
        *                                ) break                                       ;;
    esac
done

if [ ! -d "${PYTHON_DISTRIBUTE_SOURCE_DIR}" ]; then
    mkdir -p "${PYTHON_DISTRIBUTE_SOURCE_DIR}"
    wget -O "${BUILD_TEMP_DIR}/python-distribute.tar.gz" "${PYTHON_DISTRIBUTE_SOURCE_URL}"
    tar -xzvf "${BUILD_TEMP_DIR}/python-distribute.tar.gz" -C "${BUILD_TEMP_DIR}"
    mv "${BUILD_TEMP_DIR}"/distribute-*/* "${PYTHON_DISTRIBUTE_SOURCE_DIR}"
fi

if [ ! -f "${PYTHON_DISTRIBUTE_SOURCE_DIR}/.hypernova_build_complete" ]; then
    pushd "${PYTHON_DISTRIBUTE_SOURCE_DIR}"
    "${PYTHON_BINARY}" ./setup.py bdist_egg
    touch ".hypernova_build_complete"
    popd
fi

exit 0

