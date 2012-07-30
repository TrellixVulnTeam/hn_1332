#
# HyperNova server management framework
#
# RPM specification for the HyperNova Python distribution
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

Name:    hypernova-python
Version: %version
Release: %{?dist}
Summary: HyperNova's self-contained Python installation

Group:   Development/Languages
License: PSF License
URL:     http://python.org/

%description
An entirely self-contained Python interpreter for use with the HyperNova
software stack.


%prep
rm -rfv "%buildroot"

%install
cd "%builddir"
make install DESTDIR="%buildroot%prefixdir"


%files
%defattr(-, root, root, -)
%prefixdir

