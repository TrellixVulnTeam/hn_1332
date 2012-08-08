#
# HyperNova server management framework
#
# RPM specification for the HyperNova Phing Deploy distribution
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

Name:    hypernova-phing-deploy
Version: %version
Release: %{?dist}
Summary: HyperNova's Phing deployment tools and packages

Group:   Development/Languages
License: PSF License
URL:     http://python.org/


%description
An entirely self-contained Phing interpreter for use with the HyperNova
software stack in order to deploy PHP web sites.


%prep
rm -rfv "%buildroot"


%install
cd "%builddir"
make install DESTDIR="%buildroot%prefixdir"


%files
%defattr(-, root, root, -)
%prefixdir

