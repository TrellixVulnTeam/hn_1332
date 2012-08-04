#
# HyperNova server management framework
#
# RPM specification for the HyperNova Python Distribute module distribution
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

Name:    hypernova-core
Version: %modversion
Release: %{?dist}
Summary: HyperNova server management framework

Group:   Application/Internet
License: LGPL
URL:     http://dev.ossservices.com/projects/cloudnova-hypernova


%description
Server management framework and provisioning system designed for large scale
hosting operations.


%prep
rm -rfv "%buildroot"


%install
pushd "%pythonbuilddir"
make install DESTDIR="%buildroot%prefixdir"
popd

pushd "%distributebuilddir"
"%buildroot%prefixdir/bin/python3.2" ./setup.py install
popd

pushd "%builddir"
"%buildroot%prefixdir/bin/python3.2" ./setup.py install
popd

shopt -s extglob
rm -rfv "%buildroot%prefixdir"/!(lib*)
rm -rfv "%buildroot%prefixdir"/lib*/!(python*)
rm -rfv "%buildroot%prefixdir"/lib*/python*/!("site-packages")
rm -rfv "%buildroot%prefixdir"/lib*/python*/"site-packages"/!(HyperNova-*)

pushd "%venvdir"
mkdir -p "%buildroot%prefixdir"/{"bin","etc","var/lib/platforms"}
cp -R "bin"/hn-* "%buildroot%prefixdir/bin"
cp -R "etc"/* "%buildroot%prefixdir/etc"
cp -R "var/lib/platforms"/* "%buildroot%prefixdir/var/lib/platforms"
popd


%files
%defattr(-, root, root, -)
%prefixdir

