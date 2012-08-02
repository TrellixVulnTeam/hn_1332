#!/bin/bash
[ "X`which qemu-system-x86_64`" = "X" ] && echo "qemu-system-x86_64  should be installed on your system" && exit 0
[ ! -e centos-6.2.img ] && scp dev.ossservices.com:/srv/centos-6.2.img.gz . && echo "Downloading the image" && gunzip centos-6.2.img.gz


# Run the build system
[ ! -e node.img ] && qemu-img create -f qcow2 -b centos-6.2.img node.img && echo "Creating the node image..." 

echo "Launch the VM to build HyperNova Package: will be use for the manager AND the client"
echo "Running emulator. You can ssh into it from the port 3333"
qemu-system-x86_64 -m 512 -net nic,macaddr=52:54:00:f5:80:66 -net user -hda node.img  -enable-kvm -redir tcp:3333::22 -nographic &
QEMU_PID=$!

until `ssh -l hnbuild localhost -p 3333 exit` ; do echo -n "."; done


scp -P 3333 -r RPMS/ hnbuild@localhost:/home/hnbuild/hypernova/

expect -f installAgent.tcl

#kill $QEMU_PID


