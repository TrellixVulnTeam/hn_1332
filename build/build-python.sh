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

eval set -- "$(getopt -o "dtu:" --long "python-source-dir:,build-temp-dir:,python-source-url:" -- "$@")"
while true; do
    case "$1" in
        -d|--python-source-dir) PYTHON_SOURCE_DIR="$2" ; shift 2 ;;
        -t|--build-temp-dir   ) BUILD_TEMP_DIR="$2"    ; shift 2 ;;
        -u|--python-source-url) PYTHON_SOURCE_URL="$2" ; shift 2 ;;
        *                     ) break                             ;;
    esac
done

if [ ! -d "${PYTHON_SOURCE_DIR}" ]; then
    mkdir -p "${PYTHON_SOURCE_DIR}"
    wget -O "${BUILD_TEMP_DIR}/python.tar.bz2" "${PYTHON_SOURCE_URL}"
    tar -xjvf "${BUILD_TEMP_DIR}/python.tar.bz2" -C "${BUILD_TEMP_DIR}"
    mv "${BUILD_TEMP_DIR}"/Python-*/* "${PYTHON_SOURCE_DIR}"
fi

if [ ! -f "${PYTHON_SOURCE_DIR}/.hypernova_build_complete" ]; then
    pushd "${PYTHON_SOURCE_DIR}"
    ./configure --prefix=
    make
    touch ".hypernova_build_complete"
    popd
fi

exit 0

