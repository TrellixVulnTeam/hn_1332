#!/bin/sh
[ "X`which qemu-system-x86_64`" = "X" ] && echo "qemu-system-x86_64  should be installed on your system" && exit 0
[ ! -e centos-6.2.img ] && scp dev.ossservices.com:/srv/centos-6.2.img.gz . && echo "Downloading the image" && gunzip centos-6.2.img.gz


# Run the build system
[ ! -e manager.img ] && qemu-img create -f qcow2 -b centos-6.2.img manager.img && echo "Creating the manager image..." 
[ ! -e node.img ] && qemu-img create -f qcow2 -b centos-6.2.img node.img && echo "Creating the node image..." 

echo "Running emulator. You can ssh into it from the port 3333"
# For Mac address see /etc/udev rules, we have 2 interfaces eth0=..66 and eth1=...56
qemu-system-x86_64 -m 512 -net nic,model=ne2k_pci,macaddr=52:54:00:f5:80:66  -net socket,listen=:6070  -net nic,model=ne2k_pci -net user -redir tcp:3333::22 -hda manager.img  -enable-kvm  &
qemu-system-x86_64 -m 512 -net nic,model=ne2k_pci,macaddr=52:54:00:12:34:56  -net socket,connect=127.0.0.1:6070  -hda node.img  -enable-kvm &

#qemu-system-x86_64 -m 512 -net nic,macaddr=52:54:00:f5:80:66 -net user,dhcpstart=10.0.2.15 -redir tcp:3333::22 -net socket,listen=:6070 -hda manager.img  -enable-kvm  &
#qemu-system-x86_64 -m 512 -net nic,macaddr=52:54:00:12:34:56 -net user -redir tcp:4444::22  -net socket,connect=127.0.0.1:6070 -hda node.img  -enable-kvm &

read KEY
# Run the target server system
#echo "Launch the VM as a target install for HyperNova"
#qemu-img create -f qcow2 -b centos-6.0.img builder.img 

