#!/bin/sh
[ "X`which qemu-system-x86_64`" = "X" ] && echo "qemu-system-x86_64  should be installed on your system" && exit 0

qemu-img create -f qcow2 -b centos-6.0.img test.img 

echo "Running emulator. You can ssh into it from the port 2222"
qemu-system-x86_64 -m 512 -net nic -net user -hda test.img  -enable-kvm -redir tcp:2222::22

