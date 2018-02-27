#!/bin/bash

apt-get install zlib1g-dev libssl-dev libavl-dev libev-dev coreutils acl valgrind autoconf libtool
apt-get install gcc make cmake doxygen swig python-dev lua5.2 git build-essential devscripts debhelper
apt-get install bison flex libpcre3-dev libprotobuf-c-dev protobuf-c-compiler python-codecov

echo "Building cmocka library from source"
git clone git://git.cryptomilk.org/projects/cmocka.git
cd cmocka && mkdir build && cd build
cmake .. && make -j8 && make install
cd ../..

echo "Building libyang library from source"
git clone https://github.com/CESNET/libyang.git
cd libyang; mkdir build; cd build
cmake ..
make -j8 && make install
cd ../..

echo "Building libssh library from source"
git clone -b v0-7 git://git.libssh.org/projects/libssh.git
cd libssh; mkdir build; cd build
cmake .. && make -j8 && make install
cd ../..

echo "Building libnetconf2 library from source"
git clone -b devel https://github.com/CESNET/libnetconf2.git
cd libnetconf2; mkdir build; cd build
cmake ..
make -j8 && make install
cd ../..

echo "Building protobuf library from source"
git clone https://github.com/google/protobuf.git
cd protobuf
./autogen.sh
./configure
make -j8 && make install
cd ..

echo "Building sysrepo library from source"
git clone https://github.com/sysrepo/sysrepo.git
cd sysrepo; mkdir build; cd build
cmake ..
make -j8 && make install
cd ../..

echo "Building Netopeer2 from source"
git clone https://github.com/CESNET/Netopeer2.git
cd Netopeer2
echo "Building keystored"
cd keystored && mkdir build && cd build
sysrepoctl --install --yang=/root/sysrepo/build/repository/yang/ietf-keystore@2016-10-31.yang --owner=root:root --permissions=666
cmake ..
make && make install 
cd ../..
echo "Building server"
cd server && mkdir build && cd build
cmake ..
make && make install
cd ../..
echo "Building client"
cd cli && mkdir build && cd build
cmake ..
make -j8 && make install && cd