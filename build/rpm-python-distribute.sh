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

eval set -- "$(getopt -o "bfoprsv:" --long "rpm-build-dir:,rpm-spec-dir:,rpm-output-dir:,python-source-dir:,python-distribute-rpm-prefix:,python-distribute-source-dir:,python-distribute-version:" -- "$@")"
while true; do
    case "$1" in
        -b|--rpm-build-dir                ) RPM_BUILD_DIR="$2"                 ; shift 2 ;;
        -f|--rpm-spec-dir                 ) RPM_SPEC_DIR="$2"                  ; shift 2 ;;
        -o|--rpm-output-dir               ) RPM_OUTPUT_DIR="$2"                ; shift 2 ;;
        -p|--python-source-dir            ) PYTHON_SOURCE_DIR="$2"             ; shift 2 ;;
        -r|--python-distribute-rpm-prefix ) PYTHON_DISTRIBUTE_RPM_PREFIX="$2"  ; shift 2 ;;
        -s|--python-distribute-source-dir ) PYTHON_DISTRIBUTE_SOURCE_DIR="$2"  ; shift 2 ;;
        -v|--python-distribute-version    ) PYTHON_DISTRIBUTE_VERSION="$2"     ; shift 2 ;;
        *                                 ) break                                        ;;
    esac
done

arch="$(rpm --eval "%_arch")"
dist="$(rpm --eval "%dist")"
rpm="${RPM_OUTPUT_DIR}/${arch}/hypernova-python-distribute-${PYTHON_DISTRIBUTE_VERSION}-${dist}.${arch}.rpm"

if [ ! -f "${rpm}" ]; then
    pushd "${PYTHON_DISTRIBUTE_SOURCE_DIR}"
    rpmbuild \
        -bb -vv \
        --define "_topdir        ${RPM_BUILD_DIR}" \
        --define "_rpmdir        ${RPM_OUTPUT_DIR}" \
        --define "_specdir       ${RPM_SPEC_DIR}" \
        --define "builddir       ${PYTHON_DISTRIBUTE_SOURCE_DIR}" \
        --define "pythonbuilddir ${PYTHON_SOURCE_DIR}" \
        --define "prefixdir      ${PYTHON_DISTRIBUTE_RPM_PREFIX}" \
        --define "version        ${PYTHON_DISTRIBUTE_VERSION}" \
         "${RPM_SPEC_DIR}/rpm-python-distribute.spec"
    popd
fi

exit 0

