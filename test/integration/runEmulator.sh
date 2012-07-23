#!/bin/sh
[ "X`which qemu-system-x86_64`" = "X" ] && echo "qemu-system-x86_64  should be installed on your system" && exit 0
[ ! -e centos-6.2.img ] && scp dev.ossservices.com:/srv/centos-6.2.img.gz . && echo "Downloading the image" && gunzip centos-6.2.img.gz


# Run the build system
[ ! -e manager.img ] && qemu-img create -f qcow2 -b centos-6.2.img manager.img && echo "Creating the manager image..." 
[ ! -e node.img ] && qemu-img create -f qcow2 -b centos-6.2.img node.img && echo "Creating the node image..." 

echo "Running emulator. You can ssh into it from the port 3333"
# from http://tjworld.net/wiki/Linux/KvmQemuEasyRoutedNetwork
WAN_IF=eth0
VMNET_GATEWAY_IF=$WAN_IF:0
VMNET_GATEWAY_IP=`ip addr list $WAN_IF |grep 'inet[^6]' | cut -d' ' -f6 | cut -d/ -f1`
VMNET_NETMASK=`ip addr list $WAN_IF |grep 'inet[^6]' | cut -d' ' -f8 | cut -d/ -f1`
VMNET_BROADCAST=`ip addr list $WAN_IF |grep 'inet[^6]' | cut -d' ' -f6 | cut -d/ -f1`
VMNET_FIRST_GUEST_IP=10.254.254.2
# set to 0 to disable; 1 to enable
PROXY_ARP=1
sudo ifconfig $VMNET_GATEWAY_IF $VMNET_GATEWAY_IP netmask $VMNET_NETMASK broadcast $VMNET_BROADCAST
sudo sh -c "echo 1 > /proc/sys/net/ipv4/conf/${WAN_IF}/forwarding"
sudo sh -c "echo $PROXY_ARP > /proc/sys/net/ipv4/conf/${WAN_IF}/proxy_arp"
# interface numbers start at 0. GUEST_MAX=1 will create 1 interface: tap0
GUEST_MAX=2
IP=$VMNET_FIRST_GUEST_IP

# Double parentheses, and "GUEST_MAX" with no "$"
for ((IF=0; IF < GUEST_MAX ; IF++)); do
 # create the persistent tap interface
 sudo tunctl -t tap${IF} -u `id -un` -g `id -gn`
 # start the interface
 sudo ip link set tap${IF} up
 # configure proxy_arp according to the environment variable setting
 sudo sh -c "echo $PROXY_ARP > /proc/sys/net/ipv4/conf/tap${IF}/proxy_arp"
 # route packets destined for the VM guest's IP address to this interface
 sudo /sbin/ip route add unicast $IP dev tap${IF}
 # figure out the IP address the next VM guest will use (increments the least-significant byte)
 IP=$(echo $IP | awk '{split($0 ,parts, "."); for(i=1;i<=3;i++) { printf("%d.", parts[i]);} print ++parts[4];}')
done
# For Mac address see /etc/udev rules, we have 2 interfaces eth0=..66 and eth1=...56
#qemu-system-x86_64 -m 512 -net nic,model=ne2k_pci,macaddr=52:54:00:f5:80:66  -net socket,listen=:6070  -hda manager.img  -enable-kvm  &
#qemu-system-x86_64 -m 512 -net nic,model=ne2k_pci,macaddr=52:54:00:12:34:56  -net socket,connect=127.0.0.1:6070  -hda node.img  -enable-kvm &

qemu-system-x86_64 -m 512 -net nic,model=ne2k_pci,macaddr=52:54:00:f5:80:66  -net tap,ifname=tap0  -hda manager.img  -enable-kvm  &
qemu-system-x86_64 -m 512 -net nic,model=ne2k_pci,macaddr=52:54:00:12:34:56  -net tap,ifname=tap0  -hda node.img  -enable-kvm &

#qemu-system-x86_64 -m 512 -net nic,macaddr=52:54:00:f5:80:66 -net user,dhcpstart=10.0.2.15 -redir tcp:3333::22 -net socket,listen=:6070 -hda manager.img  -enable-kvm  &
#qemu-system-x86_64 -m 512 -net nic,macaddr=52:54:00:12:34:56 -net user -redir tcp:4444::22  -net socket,connect=127.0.0.1:6070 -hda node.img  -enable-kvm &

read KEY
# Run the target server system
#echo "Launch the VM as a target install for HyperNova"
#qemu-img create -f qcow2 -b centos-6.0.img builder.img 

