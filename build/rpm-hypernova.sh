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

eval set -- "$(getopt -o "bdfoprsvV:" --long "rpm-build-dir:,python-distribute-source-dir:,rpm-spec-dir:,rpm-output-dir:,python-source-dir:,hypernova-rpm-prefix:,hypernova-source-dir:,hypernova-version:,hypernova-venv-dir:" -- "$@")"
while true; do
    case "$1" in
        -b|--rpm-build-dir               ) RPM_BUILD_DIR="$2"                ; shift 2 ;;
        -d|--python-distribute-source-dir) PYTHON_DISTRIBUTE_SOURCE_DIR="$2" ; shift 2 ;;
        -f|--rpm-spec-dir                ) RPM_SPEC_DIR="$2"                 ; shift 2 ;;
        -o|--rpm-output-dir              ) RPM_OUTPUT_DIR="$2"               ; shift 2 ;;
        -p|--python-source-dir           ) PYTHON_SOURCE_DIR="$2"            ; shift 2 ;;
        -r|--hypernova-rpm-prefix        ) HYPERNOVA_RPM_PREFIX="$2"         ; shift 2 ;;
        -s|--hypernova-source-dir        ) HYPERNOVA_SOURCE_DIR="$2"         ; shift 2 ;;
        -v|--hypernova-version           ) HYPERNOVA_VERSION="$2"            ; shift 2 ;;
        -V|--hypernova-venv-dir          ) HYPERNOVA_VENV_DIR="$2"           ; shift 2 ;;
        *                                ) break                                       ;;
    esac
done

arch="$(rpm --eval "%_arch")"
dist="$(rpm --eval "%dist")"
rpm="${RPM_OUTPUT_DIR}/${arch}/hypernova-core-${HYPERNOVA_VERSION}-${dist}.${arch}.rpm"

if [ ! -f "${rpm}" ]; then
    [ -z "${PYTHON_DISTRIBUTE_SOURCE_DIR}" ] && PYTHON_DISTRIBUTE_SOURCE_DIR=x
    pushd "${HYPERNOVA_SOURCE_DIR}"
    rpmbuild \
        -bb -vv \
        --define "_topdir            ${RPM_BUILD_DIR}" \
        --define "_rpmdir            ${RPM_OUTPUT_DIR}" \
        --define "_specdir           ${RPM_SPEC_DIR}" \
        --define "builddir           ${HYPERNOVA_SOURCE_DIR}" \
        --define "distributebuilddir ${PYTHON_DISTRIBUTE_SOURCE_DIR}" \
        --define "modversion         ${HYPERNOVA_VERSION}" \
        --define "pythonbuilddir     ${PYTHON_SOURCE_DIR}" \
        --define "prefixdir          ${HYPERNOVA_RPM_PREFIX}" \
        --define "venvdir            ${HYPERNOVA_VENV_DIR}" \
        "${RPM_SPEC_DIR}/rpm-hypernova.spec"
    popd
fi

exit 0

