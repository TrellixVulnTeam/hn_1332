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

eval set -- "$(getopt -o "bpsv:" --long "python-binary:,python-sitepackages-dir:,python-distribute-source-dir:,python-distribute-venv-prefix:" -- "$@")"
while true; do
    case "$1" in
        -b|--python-binary                ) PYTHON_BINARY="$2"                 ; shift 2 ;;
        -p|--python-sitepackages-dir      ) PYTHON_SITEPACKAGES_DIR="$2"       ; shift 2 ;;
        -s|--python-distribute-source-dir ) PYTHON_DISTRIBUTE_SOURCE_DIR="$2"  ; shift 2 ;;
        -v|--python-distribute-venv-prefix) PYTHON_DISTRIBUTE_VENV_PREFIX="$2" ; shift 2 ;;
        *                                 ) break                                        ;;
    esac
done

if [ ! -d "${PYTHON_SITEPACKAGES_DIR}/distribute-0.6.28-py3.2.egg" ]; then
    pushd "${PYTHON_DISTRIBUTE_SOURCE_DIR}"
    "${PYTHON_BINARY}" ./setup.py install
    popd
fi

exit 0

