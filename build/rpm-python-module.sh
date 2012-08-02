#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Python Distribute module RPM package assembly tool
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

cd "$(dirname "$(readlink -fn "$0")")"
. core.sh

trap error_trap 1 2 3 15 ERR

eval set -- "$(getopt -o "bdDfnoprsv:" --long "rpm-build-dir:,python-distribute-source-dir:,python-module-st-name:,rpm-spec-dir:,python-module-name:,rpm-output-dir:,python-source-dir:,python-module-rpm-prefix:,python-module-source-dir:,python-module-version:" -- "$@")"
while true; do
    case "$1" in
        -b|--rpm-build-dir               ) RPM_BUILD_DIR="$2"                ; shift 2 ;;
        -d|--python-distribute-source-dir) PYTHON_DISTRIBUTE_SOURCE_DIR="$2" ; shift 2 ;;
        -D|--python-module-st-name       ) PYTHON_MODULE_ST_NAME="$2"        ; shift 2 ;;
        -f|--rpm-spec-dir                ) RPM_SPEC_DIR="$2"                 ; shift 2 ;;
        -n|--python-module-name          ) PYTHON_MODULE_NAME="$2"           ; shift 2 ;;
        -o|--rpm-output-dir              ) RPM_OUTPUT_DIR="$2"               ; shift 2 ;;
        -p|--python-source-dir           ) PYTHON_SOURCE_DIR="$2"            ; shift 2 ;;
        -r|--python-module-rpm-prefix    ) PYTHON_MODULE_RPM_PREFIX="$2"     ; shift 2 ;;
        -s|--python-module-source-dir    ) PYTHON_MODULE_SOURCE_DIR="$2"     ; shift 2 ;;
        -v|--python-module-version       ) PYTHON_MODULE_VERSION="$2"        ; shift 2 ;;
        *                                ) break                                       ;;
    esac
done

arch="$(rpm --eval "%_arch")"
dist="$(rpm --eval "%dist")"
rpm="${RPM_OUTPUT_DIR}/${arch}/hypernova-python-${PYTHON_MODULE_NAME}-${PYTHON_MODULE_VERSION}-${dist}.${arch}.rpm"

if [ ! -f "${rpm}" ]; then
    [ -z "${PYTHON_DISTRIBUTE_SOURCE_DIR}" ] && PYTHON_DISTRIBUTE_SOURCE_DIR=x
    pushd "${PYTHON_MODULE_SOURCE_DIR}"
    rpmbuild \
        -bb -vv \
        --define "_topdir            ${RPM_BUILD_DIR}" \
        --define "_rpmdir            ${RPM_OUTPUT_DIR}" \
        --define "_specdir           ${RPM_SPEC_DIR}" \
        --define "builddir           ${PYTHON_MODULE_SOURCE_DIR}" \
        --define "modname            ${PYTHON_MODULE_NAME}" \
        --define "modversion         ${PYTHON_MODULE_VERSION}" \
        --define "pythonbuilddir     ${PYTHON_SOURCE_DIR}" \
        --define "prefixdir          ${PYTHON_MODULE_RPM_PREFIX}" \
        --define "distributebuilddir ${PYTHON_DISTRIBUTE_SOURCE_DIR}" \
        --define "modstname          ${PYTHON_MODULE_ST_NAME}" \
        "${RPM_SPEC_DIR}/rpm-python-module.spec"
    popd
fi

exit 0

