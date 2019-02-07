#!/bin/bash

set -e

# Get the number of available cores to speed up the build
COUNT_CORES=`grep -c ^processor /proc/cpuinfo`
echo "Will use $COUNT_CORES parallel jobs to build DCMTK"

apt install git

cd /root/
git clone https://github.com/DCMTK/dcmtk
cd dcmtk
mkdir Build
cd Build
cmake .. -DBUILD_SHARED_LIBS=ON -DBUILD_APPS=ON -DCMAKE_INSTALL_PREFIX=/usr/
make -j$COUNT_CORES
make install

# Remove the build directory to recover space
cd /root/
rm -rf /root/dcmtk