#
# HyperNova server management framework
#
# RPM specification for the HyperNova Python Distribute module distribution
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

Name:    hypernova-python-%modname
Version: %modversion
Release: %{?dist}
Summary: Distribute module for HyperNova's self-contained Python installation

Group:   Development/Languages
License: PSF License; ZPL License
URL:     http://pypi.python.org/pypi/distribute/


%description
An installation of the Distribute packaging module built specifically for the
entirely self-contained Python interpreter for use with the HyperNova software
stack.


%prep
rm -rfv "%buildroot"


%install
pushd "%pythonbuilddir"
make install DESTDIR="%buildroot%prefixdir"
popd

if [ "%modname" != "distribute" ]; then
    pushd "%distributebuilddir"
    "%buildroot%prefixdir/bin/python3.2" ./setup.py install
    popd
fi

pushd "%builddir"
"%buildroot%prefixdir/bin/python3.2" ./setup.py install
popd

shopt -s extglob
rm -rfv "%buildroot%prefixdir"/!(lib*)
rm -rfv "%buildroot%prefixdir"/lib*/!(python*)
rm -rfv "%buildroot%prefixdir"/lib*/python*/!("site-packages")
rm -rfv "%buildroot%prefixdir"/lib*/python*/"site-packages"/!(%modstname-*)


%files
%defattr(-, root, root, -)
%prefixdir/lib*/python*/site-packages/%modstname-*

