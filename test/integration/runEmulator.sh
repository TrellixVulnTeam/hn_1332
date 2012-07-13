#!/bin/sh
[ "X`which qemu-system-x86_64`" = "X" ] && echo "qemu-system-x86_64  should be installed on your system" && exit 0
[ ! -e centos-6.2.img ] && scp dev.ossservices.com:/srv/centos-6.2.img.gz . && echo "Downloading the image" && gunzip centos-6.2.img.gz


# Run the build system
[ ! -e manager.img ] && qemu-img create -f qcow2 -b centos-6.2.img manager.img && echo "Creating the manager image..." 
[ ! -e node.img ] && qemu-img create -f qcow2 -b centos-6.2.img node.img && echo "Creating the node image..." 

echo "Running emulator. You can ssh into it from the port 2222"
qemu-system-x86_64 -m 512 -net nic -net socket,vlan=1,listen=:8010 -hda manager.img  -enable-kvm  &
qemu-system-x86_64 -m 512 -net nic -net socket,vlan=1,connect=connect=127.0.0.1:8010 -hda node.img  -enable-kvm  &

# Run the target server system
#echo "Launch the VM as a target install for HyperNova"
#qemu-img create -f qcow2 -b centos-6.0.img builder.img 

