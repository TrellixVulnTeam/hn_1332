#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Core functionality required by the build scripts
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

# Error trap
#   If a command fails, exit the script cleanly.
error_trap () {
    local exit_status=${1:-$?}
    echo "Command returned non-zero (${exit_status}) exit status; aborting"
    exit "${exit_status}"
}

