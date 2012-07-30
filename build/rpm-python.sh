#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Python RPM package assembly tool
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

cd "$(dirname "$(readlink -fn "$0")")"
. core.sh

trap error_trap 1 2 3 15 ERR

eval set -- "$(getopt -o "bfprsv:" --long "rpm-build-dir:,rpm-spec-dir:,python-rpm-prefix:,python-source-dir:,rpm-output-dir:,python-version:" -- "$@")"
while true; do
    case "$1" in
        -b|--rpm-build-dir     ) RPM_BUILD_DIR="$2"      ; shift 2 ;;
        -f|--rpm-spec-dir      ) RPM_SPEC_DIR="$2"       ; shift 2 ;;
        -i|--python-install-dir) PYTHON_INSTALL_DIR="$2" ; shift 2 ;;
        -r|--python-rpm-prefix ) PYTHON_RPM_PREFIX="$2"  ; shift 2 ;;
        -r|--rpm-output-dir    ) RPM_OUTPUT_DIR="$2"     ; shift 2 ;;
        -s|--python-source-dir ) PYTHON_SOURCE_DIR="$2"  ; shift 2 ;;
        -v|--python-version    ) PYTHON_VERSION="$2"     ; shift 2 ;;
        *                      ) break                             ;;
    esac
done

arch="$(rpm --eval "%_arch")"
dist="$(rpm --eval "%dist")"
rpm="${RPM_OUTPUT_DIR}/${arch}/hypernova-python-${PYTHON_VERSION}-1${dist}.${arch}.rpm"

if [ ! -f "${rpm}" ]; then
    pushd "${PYTHON_SOURCE_DIR}"
    export PYTHON_RPM_PREFIX
    rpmbuild \
        -bb -vv \
        --define "_topdir   ${RPM_BUILD_DIR}" \
        --define "_rpmdir   ${RPM_OUTPUT_DIR}" \
        --define "_specdir  ${RPM_SPEC_DIR}" \
        --define "builddir  ${PYTHON_SOURCE_DIR}" \
        --define "prefixdir ${PYTHON_RPM_PREFIX}" \
         "${RPM_SPEC_DIR}/rpm-python.spec"
    popd
fi

exit 0

