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

ELEVATOR_VERSION     := 0.1.0
ELEVATOR_SOURCE_DIR  := $(BUILD_ROOT_DIR)/deps/elevator
ELEVATOR_RPM_PREFIX  := /usr/local/hypernova
ELEVATOR_VENV_PREFIX := $(BUILD_ROOT_DIR)/chroot

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
	@echo '| build-elevator  | build just Elevator                            |'
	@echo '| build-python    | build just Python                              |'
	@echo '| clean           | clean all build artefacts                      |'
	@echo '| clean-elevator  | clean just Elevator build artefacts            |'
	@echo '| clean-python    | clean just Python build artefacts              |'
	@echo '| rpm             | generate RPM packages of HyperNova and deps    |'
	@echo '| rpm-elevator    | generate RPM packages of just Elevator         |'
	@echo '| rpm-python      | generate RPM packages of just Python           |'
	@echo '| venv            | build the tree and install it to a virtualenv  |'
	@echo '| venv-elevator   | build and install just Elevator                |'
	@echo '| venv-python     | build and install just Python                  |'
	@echo '+-----------------+------------------------------------------------+'

build: build-elevator build-python

build-elevator:
	$(BUILD_ROOT_DIR)/build/build-elevator.sh \
		--elevator-source-dir $(ELEVATOR_SOURCE_DIR)

build-python:
	$(BUILD_ROOT_DIR)/build/build-python.sh \
		--build-temp-dir $(BUILD_TEMP_DIR) \
		--python-source-url $(PYTHON_SOURCE_URL) \
		--python-source-dir $(PYTHON_SOURCE_DIR)

clean: clean-elevator clean-python

clean-elevator:
	$(BUILD_ROOT_DIR)/build/clean-elevator.sh \
		--elevator-source-dir $(ELEVATOR_SOURCE_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR)

clean-python:
	$(BUILD_ROOT_DIR)/build/clean-python.sh \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR)

rpm: rpm-elevator rpm-python

rpm-elevator: build-elevator
	$(BUILD_ROOT_DIR)/build/rpm-elevator.sh \
		--elevator-rpm-prefix $(ELEVATOR_RPM_PREFIX) \
		--elevator-source-dir $(ELEVATOR_SOURCE_DIR) \
		--elevator-version $(ELEVATOR_VERSION) \
		--rpm-build-dir $(RPM_BUILD_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR) \
		--rpm-spec-dir $(RPM_SPEC_DIR)

rpm-python: build-python
	$(BUILD_ROOT_DIR)/build/rpm-python.sh \
		--python-rpm-prefix $(PYTHON_RPM_PREFIX) \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--python-version $(PYTHON_VERSION) \
		--rpm-build-dir $(RPM_BUILD_DIR) \
		--rpm-output-dir $(RPM_OUTPUT_DIR) \
		--rpm-spec-dir $(RPM_SPEC_DIR)

venv: venv-elevator venv-python

venv-elevator: build-elevator
	$(BUILD_ROOT_DIR)/build/venv-elevator.sh \
		--elevator-source-dir $(ELEVATOR_SOURCE_DIR) \
		--elevator-venv-prefix $(ELEVATOR_VENV_PREFIX)

venv-python: build-python
	$(BUILD_ROOT_DIR)/build/venv-python.sh \
		--python-source-dir $(PYTHON_SOURCE_DIR) \
		--python-venv-prefix $(PYTHON_VENV_PREFIX)

