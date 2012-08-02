#!/bin/sh
[ "X`which qemu-system-x86_64`" = "X" ] && echo "qemu-system-x86_64  should be installed on your system" && exit 0
[ ! -e centos-6.2.img ] && scp dev.ossservices.com:/srv/centos-6.2.img.gz . && echo "Downloading the image" && gunzip centos-6.2.img.gz


# Run the build system
[ ! -e builder.img ] && qemu-img create -f qcow2 -b centos-6.2.img builder.img && echo "Creating the builder image..." 

echo "Launch the VM to build HyperNova Package: will be use for the build"
echo "Running emulator. You can ssh into it from the port 3333"
qemu-system-x86_64 -m 512 -net nic,macaddr=52:54:00:f5:80:66 -net user -hda builder.img  -enable-kvm -redir tcp:3333::22 -nographic &
QEMU_PID=$!

# -nographic -no-acpi  ?
until `ssh -l hnbuild localhost -p 3333 exit` ; do echo -n "."; done

echo "Running the build"
../../install/rhel-push.sh -H localhost -U hnbuild -P 3333
# Copy the result
scp -P 3333 -r hnbuild@localhost:/home/hnbuild/hypernova/install/build/RPMS/ .
# Run the target server system
#echo "Launch the VM as a target install for HyperNova"
#qemu-img create -f qcow2 -b centos-6.0.img builder.img 

kill $QEMU_PID
