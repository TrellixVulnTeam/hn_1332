#!/usr/bin/env bash
#
# HyperNova server management framework
#
# Build the SRPM/RPMs
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

Name:    hypernova
Version: 0.1.0
Release: 1%{?dist}
Summary: Secure server management and site provisioning suite

Group:     Applications/Internet
License:   TDM Internal
URL:       http://dev.ossservices.com/projects/cloudnova-hypernova

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: bzip2, gcc, make, openssl-devel, pcre-devel, sed, tar, zlib-devel

Requires: hypernova-elevator hypernova-python hypernova-python-distribute
Requires: hypernova-python-gnupg

Source0: hypernova.tar.bz2
Source1: python.tar.bz2
Source2: elevator.tar.bz2
Source3: python-gnupg.tar.bz2
Source4: python-distribute.tar.bz2

%description
Secure server management and site provisioning suite.


%package elevator
Summary: user-locked permission elevation utility
Group:   Applications/Security


%description elevator
Elevator provides the ability for normal, non-privileged users to run system
applications under the privileges of an administrative user.


%package python
Summary: Locked down Python installation
Group:   Development/Languages


%description python
Python is a programming language that lets you work more quickly and integrate
your systems more effectively. You can learn to use Python and see almost
immediate gains in productivity and lower maintenance costs.

Python runs on Windows, Linux/Unix, Mac OS X, and has been ported to the Java
and .NET virtual machines.

Python is free to use, even for commercial products, because of its OSI-approved
open source license.


%package python-distribute
Summary: Easily download, build, install, upgrade, and uninstall Python packages
Group:   Development/Languages

Requires: hypernova-python


%description python-distribute
Distribute is intended to replace Setuptools as the standard method for working
with Python module distributions.


%package python-gnupg
Summary: gnupg.py is a Python API which wraps the GNU Privacy Guard
Group:   Development/Libraries

Requires: hypernova-python hypernova-python-distribute


%description python-gnupg
The GNU Privacy Guard (gpg, or gpg.exe on Windows) is a command-line program
which provides support for programmatic access via spawning a separate process
to run it and then communicating with that process from your program.

This project implements a Python library which takes care of the internal
details and allows its users to generate and manage keys, encrypt and decrypt
data, and sign and verify messages.


%prep

# Extract the source files
#
# Our aim here is to get the following directory structure:
#
# * / - the HyperNova src directory
# * /deps - a directory containing all patched source code
# * /deps/$dep - each dependency
#
# rhel-build.sh generated (bzipped) tarballs of the source code and all of its
# dependencies, so in effect we're mirroring its structure.

# HyperNova
%setup -q -n src
mkdir deps

# Python
%setup -q -n src -T -D -a 1
mv Python-3.2.2 deps/python

# Elevator
%setup -q -n src -T -D -a 2
mv elevator deps

# GnuPG
%setup -q -n src -T -D -a 3
mv python-gnupg deps

# Distribute
%setup -q -n src -T -D -a 4
mv python-distribute deps


%build

pushd deps/python
./configure \
    --prefix=/usr/local/hypernova
make
popd

pushd deps/elevator
./configure \
    --prefix=/usr/local/hypernova \
    --allow-uid=703 \
    --allow-gid=703 \
    --target-uid=0 \
    --target-gid=0
make
popd

%install

pushd deps/python
make install DESTDIR="$RPM_BUILD_ROOT"
popd

# Hack for elevator
#
# Because of the setuid bit dependency, we _cannot_ install elevator using its
# Makefile. Instead, we copy the elevator binary from the build directory and
# apply the special privileges later (via the %files section).
pushd deps/elevator
cp build/elevator "$RPM_BUILD_ROOT/usr/local/hypernova/bin/elevator"
popd

pushd deps/python-distribute
"$RPM_BUILD_ROOT/usr/local/hypernova/bin/python3.2" setup.py install
popd

pushd deps/python-gnupg
"$RPM_BUILD_ROOT/usr/local/hypernova/bin/python3.2" setup.py install
popd

"$RPM_BUILD_ROOT/usr/local/hypernova/bin/python3.2" setup.py install

pushd ../chroot
cp -r * "$RPM_BUILD_ROOT/usr/local/hypernova"
popd


%clean
rm -rf "$RPM_BUILD_ROOT"


%files
%defattr(-, root, root, -)
                                /usr/local/hypernova/bin/hn-*
%config(noreplace)              /usr/local/hypernova/etc/hypernova/agent/agent.ini
%config(noreplace)              /usr/local/hypernova/var/lib/hypernova/platforms/*/packages.json
                                /usr/local/hypernova/lib/python*/site-packages/HyperNova-*.egg


%files elevator
%defattr(6755, root, root, -)
                                /usr/local/hypernova/bin/elevator


%files python
%defattr(-, root, root, -)
                                /usr/local/hypernova/bin/2to3*
                                /usr/local/hypernova/bin/idle*
                                /usr/local/hypernova/bin/pydoc*
                                /usr/local/hypernova/bin/python*
                                /usr/local/hypernova/include/python*
                                /usr/local/hypernova/lib/pkgconfig/python*
                                /usr/local/hypernova/lib/libpython*
                                /usr/local/hypernova/lib/python*
%exclude                        /usr/local/hypernova/lib/python*/site-packages
                                /usr/local/hypernova/share/man/man1/python*


%files python-distribute
%defattr(-, root, root, -)
                                /usr/local/hypernova/bin/easy_install*
                                /usr/local/hypernova/lib/python*/site-packages/distribute-*.egg


%files python-gnupg
%defattr(-, root, root, -)
                                /usr/local/hypernova/lib/python*/site-packages/python_gnupg*.egg
