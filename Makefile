#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Makefile wrapper for build actions
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

BUILD_ROOT_DIR := $(CURDIR)
BUILD_TEMP_DIR := $(shell mktemp -d)

PYTHON_INSTALL_DIR := $(BUILD_ROOT_DIR)/chroot
PYTHON_SOURCE_URL  := http://python.org/ftp/python/3.2.3/Python-3.2.3.tar.bz2
PYTHON_SOURCE_DIR  := $(BUILD_ROOT_DIR)/deps/python

all:
	@echo HyperNova
	@echo =========
	@echo
	@echo '+-----------------+------------------------------------------------+'
	@echo '| Target          | Description                                    |'
	@echo '+-----------------+------------------------------------------------+'
	@echo '| build           | build HyperNova and all dependencies           |'
	@echo '| build-python    | build just Python                              |'
	@echo '| clean           | clean all build artefacts                      |'
	@echo '| clean-python    | clean just Python build artefacts              |'
	@echo '| venv            | build the tree and install it to a virtualenv  |'
	@echo '| venv-python     | build and install just Python                  |'
	@echo '+-----------------+------------------------------------------------+'

build: build-python

build-python:
	$(BUILD_ROOT_DIR)/build/build-python.sh \
		--build-temp-dir $(BUILD_TEMP_DIR) \
		--python-source-url $(PYTHON_SOURCE_URL) \
		--python-source-dir $(PYTHON_SOURCE_DIR) \

clean: clean-python

clean-python:
	$(BUILD_ROOT_DIR)/build/clean-python.sh \
		--python-source-dir $(PYTHON_SOURCE_DIR) \

venv: venv-python

venv-python: build-python
	$(BUILD_ROOT_DIR)/build/venv-python.sh \
		--python-install-dir $(PYTHON_INSTALL_DIR) \
		--python-source-dir $(PYTHON_SOURCE_DIR)

