#!/bin/sh
[ "X`which qemu-system-x86_64`" = "X" ] && echo "qemu-system-x86_64  should be installed on your system" && exit 0
[ ! -e centos-6.2.img ] && scp dev.ossservices.com:/srv/centos-6.2.img.gz . && echo "Downloading the image" && gunzip centos-6.2.img.gz


# Run the build system
[ ! -e manager.img ] && qemu-img create -f qcow2 -b centos-6.2.img manager.img && echo "Creating the manager image..." 
[ ! -e node.img ] && qemu-img create -f qcow2 -b centos-6.2.img node.img && echo "Creating the node image..." 

echo "Launch the VM to build HyperNova Package: will be use for the build AND the client"
echo "Running emulator. You can ssh into it from the port 3333"
qemu-system-x86_64 -m 512 -net nic,vhost -net user -hda manager.img  -enable-kvm &
qemu-system-x86_64 -m 512 -net nic -net user -hda node.img  -enable-kvm &

until `ssh -l hnbuild localhost -p 3333 exit` ; do echo -n "."; done

echo "Running the build"
../../install/rhel-push.sh -H localhost -U hnbuild -P 3333
# Copy the result
scp -P 3333 -r hnbuild@localhost:/home/hnbuild/hypernova/install/build/RPMS/ .
# Run the target server system
#echo "Launch the VM as a target install for HyperNova"
#qemu-img create -f qcow2 -b centos-6.0.img builder.img 

