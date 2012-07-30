#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Elevator RPM package assembly tool
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

cd "$(dirname "$(readlink -fn "$0")")"
. core.sh

trap error_trap 1 2 3 15 ERR

eval set -- "$(getopt -o "bfprsv:" --long "rpm-build-dir:,rpm-spec-dir:,elevator-rpm-prefix:,elevator-source-dir:,rpm-output-dir:,elevator-version:" -- "$@")"
while true; do
    case "$1" in
        -b|--rpm-build-dir       ) RPM_BUILD_DIR="$2"        ; shift 2 ;;
        -f|--rpm-spec-dir        ) RPM_SPEC_DIR="$2"         ; shift 2 ;;
        -i|--elevator-install-dir) ELEVATOR_INSTALL_DIR="$2" ; shift 2 ;;
        -r|--elevator-rpm-prefix ) ELEVATOR_RPM_PREFIX="$2"  ; shift 2 ;;
        -r|--rpm-output-dir      ) RPM_OUTPUT_DIR="$2"       ; shift 2 ;;
        -s|--elevator-source-dir ) ELEVATOR_SOURCE_DIR="$2"  ; shift 2 ;;
        -v|--elevator-version    ) ELEVATOR_VERSION="$2"     ; shift 2 ;;
        *                        ) break                               ;;
    esac
done

arch="$(rpm --eval "%_arch")"
dist="$(rpm --eval "%dist")"
rpm="${RPM_OUTPUT_DIR}/${arch}/hypernova-elevator-${ELEVATOR_VERSION}-1${dist}.${arch}.rpm"

if [ ! -f "${rpm}" ]; then
    pushd "${ELEVATOR_SOURCE_DIR}"
    export ELEVATOR_RPM_PREFIX
    rpmbuild \
        -bb -vv \
        --define "_topdir   ${RPM_BUILD_DIR}" \
        --define "_rpmdir   ${RPM_OUTPUT_DIR}" \
        --define "_specdir  ${RPM_SPEC_DIR}" \
        --define "builddir  ${ELEVATOR_SOURCE_DIR}" \
        --define "prefixdir ${ELEVATOR_RPM_PREFIX}" \
        --define "version   ${ELEVATOR_VERSION}" \
         "${RPM_SPEC_DIR}/rpm-elevator.spec"
    popd
fi

exit 0

