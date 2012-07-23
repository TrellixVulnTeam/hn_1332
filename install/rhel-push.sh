#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Push RPMs to the local repo server
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#


# Initialisation
port="22"
with_python=""
user=hnbuild
host=localhost

function usage()
{
cat << EOF
usage: $0 options

This script will push the build scripts onto a build machine

OPTIONS:
   -h      Show this message
   -H      Host name (ssh)
   -P      Port (ssh)
   -U 	   User (ssh)	
   -y uses python
EOF
}


while getopts "hH:P:U:y" OPTION
do
     case $OPTION in
         h)
             usage;
             exit 1
             ;;
         H)
             host=$OPTARG
             ;;
         P)
             port=$OPTARG
             ;;
         U)
             user=$OPTARG
             ;;
         y)
         	with_python="--with-python"
         	;;
         ?)
             usage
             exit
             ;;
     esac
done

cd "$(dirname "$0")/.."

echo "Preparing remote build environment... [Host:$host Port:$port  User:$user $with_python]"

ssh -tt -l "$user" "$host" -p $port <<EOF
sudo yum -y install createrepo gcc make rpm-build rsync sudo wget \
                    {mysql,openssl,pcre,sqlite,zlib}-devel
mkdir -p hypernova
exit
EOF

echo "Synchronising local files with remote..."
includes=(
    "chroot"
    "deps"
    "install"
    "src"
    "support"
)

excludes=(
    "**/.git*"
    "**/.hg*"
    "**/__pycache__"
    "**/*.egg-info"
    "chroot/etc/client"
    "chroot/lib*/**"
    "deps/**/build"
    "deps/**/dist"
    "deps/**/*.egg"
    "deps/python"
    "install/build"
    "install/python"
    "src/build"
    "src/**/*.egg"
)

includes_line=""
for include in ${includes[@]}; do
    includes_line="${includes_line}${include} "
done

excludes_line=""
for exclude in ${excludes[@]}; do
    excludes_line="${excludes_line}--exclude ${exclude} "
done

rsync -arvuz --delete{,-excluded} $includes_line$excludes_line  -e "ssh  -p ${port} " ${user}@${host}:/home/${user}/hypernova

echo "performing the build..."
ssh -tt -l "$user" "$host" -p $port <<EOF
export hypernova_build_arch="\$(rpm --eval %{_arch})"
hypernova/install/rhel-build.sh "$with_python"
rm -rf rpms/RPMS/"\$hypernova_build_arch"/hypernova-*
mkdir -p rpms/RPMS/"\$hypernova_build_arch"
cp hypernova/install/build/RPMS/"\$hypernova_build_arch"/* \
   rpms/RPMS/"\$hypernova_build_arch"
createrepo rpms/RPMS/"\$hypernova_build_arch"
exit
EOF
