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
Release: 4%{?dist}
Summary: Secure server management and site provisioning suite

Group:     Applications/Internet
License:   TDM Internal
URL:       http://dev.ossservices.com/projects/cloudnova-hypernova

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: bzip2, findutils, gcc, make, mysql-devel, openssl-devel, pcre-devel, sed, tar, zlib-devel

# Breaks the resulting RPMs by adding incoherent dependencies (#83)
AutoReqProv: no

Requires: gpg hypernova-elevator hypernova-python hypernova-python-distribute hypernova-python-gnupg hypernova-python-oursql hypernova-python-pexpect

Source0: hypernova.tar.bz2
Source1: python.tar.bz2
Source2: elevator.tar.bz2
Source3: python-gnupg.tar.bz2
Source4: python-distribute.tar.bz2
Source5: python-oursql.tar.bz2
Source6: python-pyrg.tar.bz2
Source7: python-pexpect.tar.bz2
Source8: oss-build-system.tar.bz2


%description
Secure server management and site provisioning suite.


%package elevator
Summary: user-locked permission elevation utility
Group:   Applications/Security

# Breaks the resulting RPMs by adding incoherent dependencies (#83)
AutoReqProv: no


%description elevator
Elevator provides the ability for normal, non-privileged users to run system
applications under the privileges of an administrative user.


%package python
Summary: Locked down Python installation
Group:   Development/Languages

# Breaks the resulting RPMs by adding incoherent dependencies (#83)
AutoReqProv: no


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

# Breaks the resulting RPMs by adding incoherent dependencies (#83)
AutoReqProv: no

Requires: hypernova-python


%description python-distribute
Distribute is intended to replace Setuptools as the standard method for working
with Python module distributions.


%package python-gnupg
Summary: gnupg.py is a Python API which wraps the GNU Privacy Guard
Group:   Development/Libraries

# Breaks the resulting RPMs by adding incoherent dependencies (#83)
AutoReqProv: no

Requires: hypernova-python hypernova-python-distribute


%description python-gnupg
The GNU Privacy Guard (gpg, or gpg.exe on Windows) is a command-line program
which provides support for programmatic access via spawning a separate process
to run it and then communicating with that process from your program.

This project implements a Python library which takes care of the internal
details and allows its users to generate and manage keys, encrypt and decrypt
data, and sign and verify messages.


%package python-oursql
Summary: MySQL bindings for Python
Group:   Development/Libraries

# Breaks the resulting RPMs by adding incoherent dependencies (#83)
AutoReqProv: no


%description python-oursql
oursql is a set of MySQL bindings for python 2.4+ with a focus on wrapping the MYSQL_STMT API to provide real parameterization and real server-side cursors. MySQL 4.1.2 or better is required.

There's extensive documentation available online at http://packages.python.org/oursql/.


%package python-pyrg
Summary: Colours unittest output
Group:   Development/Libraries

# Breaks the resulting RPMs by adding incoherent dependencies (#83)
AutoReqProv: no


%description python-pyrg
This script is colourised to Python's UnitTest Result.


%package python-pexpect
Summary: Expect-like interface to interactive process I/O
Group:   Development/Libraries

%description python-pexpect
Pexpect is a pure Python module that makes Python a better tool for controlling and automating other programs. Pexpect is similar to the Don Libes `Expect` system, but Pexpect as a different interface that is easier to understand. Pexpect is basically a pattern matching system. It runs programs and watches output. When output matches a given pattern Pexpect can respond as if a human were typing responses. Pexpect can be used for automation, testing, and screen scraping. Pexpect can be used for automating interactive console applications such as ssh, ftp, passwd, telnet, etc. It can also be used to control web applications via `lynx`, `w3m`, or some other text-based web browser.

%package phing-deploy
Summary: An entirely self-contained Phing interpreter for use with the HyperNova
Group:   Development/Language
AutoReqProv: no

%description phing-deploy
An entirely self-contained Phing interpreter for use with the HyperNova
software stack in order to deploy PHP web sites.


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
mv python deps

# Elevator
%setup -q -n src -T -D -a 2
mv elevator deps

# GnuPG
%setup -q -n src -T -D -a 3
mv python-gnupg deps

# Distribute
%setup -q -n src -T -D -a 4
mv python-distribute deps

# OurSQL
%setup -q -n src -T -D -a 5
mv python-oursql deps

# pyrg
%setup -q -n src -T -D -a 6
mv python-pyrg deps

# pexpect
%setup -q -n src -T -D -a 7
mv python-pexpect deps

# phing-deploy
%setup -q -n src -T -D -a 8
mkdir deps/phing-deploy
mv oss-build-system/{*.xml,phing,buildlib,config-templates}  deps/phing-deploy

%build

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

mkdir -p "$RPM_BUILD_ROOT"

pushd deps/python
mv * "$RPM_BUILD_ROOT"
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

pushd deps/python-oursql
"$RPM_BUILD_ROOT/usr/local/hypernova/bin/python3.2" setup.py install
popd

pushd deps/python-pyrg
"$RPM_BUILD_ROOT/usr/local/hypernova/bin/python3.2" setup.py install
popd

pushd deps/python-pexpect
"$RPM_BUILD_ROOT/usr/local/hypernova/bin/python3.2" setup.py install
popd

"$RPM_BUILD_ROOT/usr/local/hypernova/bin/python3.2" setup.py install

pushd ../chroot
cp -r * "$RPM_BUILD_ROOT/usr/local/hypernova"

mkdir -p "$RPM_BUILD_ROOT/etc/profile.d"
find "$RPM_BUILD_ROOT/usr/local/hypernova/etc/profile.d" -type f \
     -exec mv {} "$RPM_BUILD_ROOT/etc/profile.d" \;
popd

# Red Hat specific files
pushd ../support/rhel
mkdir -p "$RPM_BUILD_ROOT/etc/init.d"
cp agent.init "$RPM_BUILD_ROOT/etc/init.d/hnagent"
popd

# Add directories which may not be present
mkdir -p "$RPM_BUILD_ROOT/usr/local/hypernova/var/log"
mkdir -p "$RPM_BUILD_ROOT/usr/local/hypernova/var/run"
mkdir -p "$RPM_BUILD_ROOT/usr/local/hypernova/var/lib/gpg"

# And now the files
touch "$RPM_BUILD_ROOT/usr/local/hypernova/var/run/agent.pid"


%clean
rm -rf "$RPM_BUILD_ROOT"


%post
useradd -c 'HyperNova agent' -d '/usr/local/hypernova/home' -u 703 -mU 'hnagent'

# Fix permissions.
#
# We can't set these in the files section of the spec because the user is only
# created after the files have been installed.
chown -R 'hnagent:root' '/usr/local/hypernova/var'


%postun
pkill -u 'hnagent'
userdel -r 'hnagent'


%files
%defattr(-, root, root, -)
%dir                            /usr/local/hypernova
%attr(755, root, root)          /etc/init.d/hnagent
                                /etc/profile.d/hypernova.sh
                                /usr/local/hypernova/bin/hn-*
%config(noreplace)              /usr/local/hypernova/etc/*/base.ini
%config(noreplace)              /usr/local/hypernova/var/lib/platforms/*/packages.json
                                /usr/local/hypernova/lib/python*/site-packages/HyperNova-*.egg
                                /usr/local/hypernova/var

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
                                /usr/local/hypernova/lib/python*/site-packages/python_gnupg-*.egg


%files python-oursql
%defattr(-, root, root, -)
                                /usr/local/hypernova/lib/python*/site-packages/oursql-*.egg


%files python-pyrg
%defattr(-, root, root, -)
                                /usr/local/hypernova/bin/pyrg
                                /usr/local/hypernova/lib/python*/site-packages/pyrg-*.egg


%files python-pexpect
%defattr(-, root, root, -)
                                /usr/local/hypernova/lib/python*/site-packages/pexpect-*-py3.2.egg
                                
%files phing-deploy
%defattr(-, root, root, -)
                                /usr/local/hypernova/lib/phing-deploy/phing/*
                                /usr/local/hypernova/lib/phing-deploy/build-project.xml
                                /usr/local/hypernova/lib/phing-deploy/buildlib/*
                                /usr/local/hypernova/lib/phing-deploy/config-templates/*
                     
