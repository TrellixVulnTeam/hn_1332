#
# HyperNova server management framework
#
# RPM specification for the HyperNova Elevator distribution
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

Name:    hypernova-elevator
Version: %version
Release: %{?dist}
Summary: HyperNova's self-contained Elevator installation

Group:   System Environment/Shells
License: LGPL
URL:     http://github.com/LukeCarrier/elevator


%description
An entirely self-contained utility to call another, allowing a user to run an
application within the context of another. Packaged for use with the HyperNova
stack.


%prep
rm -rfv "%buildroot"


%install
mkdir -p "%buildroot%prefixdir/bin"
cp "%builddir/build/elevator" "%buildroot%prefixdir/bin"


%files
%defattr(-, root, root, -)
%prefixdir

