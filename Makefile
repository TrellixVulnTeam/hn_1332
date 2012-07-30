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

PYTHON_VERSION     := 3.2.3
PYTHON_SOURCE_URL  := http://python.org/ftp/python/$(PYTHON_VERSION)/Python-$(PYTHON_VERSION).tar.bz2
PYTHON_SOURCE_DIR  := $(BUILD_ROOT_DIR)/deps/python
PYTHON_RPM_PREFIX  := /usr/local/hypernova
PYTHON_VENV_PREFIX := $(BUILD_ROOT_DIR)/chroot

RPM_BUILD_DIR  := $(BUILD_ROOT_DIR)/build/rpm
RPM_OUTPUT_DIR := $(BUILD_ROOT_DIR)/dist/rpm
RPM_SPEC_DIR   := $(BUILD_ROOT_DIR)/build

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
	@echo '| rpm             | generate RPM packages of HyperNova and deps    |'
	@echo '| rpm-python      | generate RPM packages of just Python           |'
	@echo '| venv            | build the tree and install it to a virtualenv  |'
	@echo '| venv-python     | build and install just Python                  |'
	@echo '+-----------------+------------------------------------------------+'

build: build-python

build-python:
	$(BUILD_ROOT_DIR)/build/build-python.sh \
		--build-temp-dir $(BUILD_TEMP_DIR) \
		--python-source-url $(PYTHON_SOURCE_URL) \
		--python-source-dir $(PYTHON_SOURCE_DIR)

clean: clean-python

clean-python:
	$(BUILD_ROOT_DIR)/build/clean-python.sh \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR)

rpm: rpm-python

rpm-python: build-python
	$(BUILD_ROOT_DIR)/build/rpm-python.sh \
		--rpm-build-dir $(RPM_BUILD_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR) \
		--rpm-spec-dir $(RPM_SPEC_DIR) \
		--python-rpm-prefix $(PYTHON_RPM_PREFIX) \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--python-version $(PYTHON_VERSION)

venv: venv-python

venv-python: build-python
	$(BUILD_ROOT_DIR)/build/venv-python.sh \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--python-venv-prefix $(PYTHON_VENV_PREFIX)

