#!/usr/bin/env bash

#
# HyperNova server management framework
#
# Push RPMs to the local repo server
#
# Copyright (c) 2012 TDM Ltd
#                    Luke Carrier <luke.carrier@tdm.info>
#

host="$1"
user="$2"
[ -n "$3" ] && with_python="--with-python"

cd "$(dirname "$0")/.."

echo "preparing remote build environment..."
ssh -tt -l "$user" "$host" <<EOF
sudo yum -y install createrepo gcc make rpm-build rsync sudo wget \
                    {mysql,openssl,pcre,sqlite,zlib}-devel
mkdir -p hypernova
exit
EOF

echo "synchronising local files with remote..."
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

rsync -arvuz --delete{,-excluded} $includes_line$excludes_line \
      "$user"@"$host":hypernova

echo "performing the build..."
ssh -tt -l "$user" "$host" <<EOF
export hypernova_build_arch="\$(rpm --eval %{_arch})"
hypernova/install/rhel-build.sh "$with_python"
rm -rf rpms/RPMS/"\$hypernova_build_arch"/hypernova-*
mkdir -p rpms/RPMS/"\$hypernova_build_arch"
cp hypernova/install/build/RPMS/"\$hypernova_build_arch"/* \
   rpms/RPMS/"\$hypernova_build_arch"
createrepo rpms/RPMS/"\$hypernova_build_arch"
exit
EOF
