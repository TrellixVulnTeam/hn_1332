#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Phing Deploy RPM package assembly tool
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

cd "$(dirname "$(readlink -fn "$0")")"
. core.sh

trap error_trap 1 2 3 15 ERR

eval set -- "$(getopt -o "bforsv:" --long "rpm-build-dir:,rpm-spec-dir:,rpm-output-dir:,rpm-prefix:,source-dir:,version:" -- "$@")"
while true; do
    case "$1" in
        -b|--rpm-build-dir     ) RPM_BUILD_DIR="$2"      ; shift 2 ;;
        -f|--rpm-spec-dir      ) RPM_SPEC_DIR="$2"       ; shift 2 ;;
        -o|--rpm-output-dir    ) RPM_OUTPUT_DIR="$2"     ; shift 2 ;;
        -r|--rpm-prefix ) PHING_DEPLOY_RPM_PREFIX="$2"  ; shift 2 ;;
        -s|--source-dir ) PHING_DEPLOY_DIR="$2"  ; shift 2 ;;
        -v|--version    ) PHING_DEPLOY_VERSION="$2"     ; shift 2 ;;
        *                      ) break                             ;;
    esac
done

arch="$(rpm --eval "%_arch")"
dist="$(rpm --eval "%dist")"
rpm="${RPM_OUTPUT_DIR}/${arch}/hypernova-phing-deploy-${PYTHON_VERSION}-${dist}.${arch}.rpm"

if [ ! -f "${rpm}" ]; then
    pushd "${PYTHON_SOURCE_DIR}"
    export PYTHON_RPM_PREFIX
    rpmbuild \
        -bb -vv \
        --define "_topdir   ${RPM_BUILD_DIR}" \
        --define "_rpmdir   ${RPM_OUTPUT_DIR}" \
        --define "_specdir  ${RPM_SPEC_DIR}" \
        --define "builddir  ${PHING_DEPLOY_SOURCE_DIR}" \
        --define "prefixdir ${PHING_DEPLOY_RPM_PREFIX}" \
        --define "version   ${PHING_DEPLOY_VERSION}" \
         "${RPM_SPEC_DIR}/rpm-phing-deploy.spec"
    popd
fi

exit 0

