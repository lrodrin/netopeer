#!/bin/bash

# update system
apt-get update -qq
# install dependencies
apt-get install -y git flex bison devscripts debhelper rpm curl autoconf build-essential nano supervisor
apt-get install -y gcc wget zlib1g-dev coreutils acl make cmake libtool pkg-config libssl-dev openssh-server
apt-get install -y libavl-dev libev-dev coreutils acl valgrind libpcre3-dev swig python-dev


echo "Building cmocka from source."
wget https://cmocka.org/files/1.1/cmocka-1.1.1.tar.xz
tar -xJvf cmocka-1.1.1.tar.xz
cd cmocka-1.1.1 && mkdir build && cd build
cmake .. && make -j2 && sudo make install
cd ../..

git clone https://github.com/CESNET/libyang.git
cd libyang; mkdir build; cd build
cmake ..
make -j2 && sudo make install
cd ../..

echo "Building libssh from source."
wget https://git.libssh.org/projects/libssh.git/snapshot/libssh-0.7.5.tar.gz
tar -xzf libssh-0.7.5.tar.gz
mkdir libssh-0.7.5/build && cd libssh-0.7.5/build
cmake .. && make -j2 && sudo make install
cd ../..

git clone https://github.com/CESNET/libnetconf2.git
cd libnetconf2; mkdir build; cd build
cmake .. && make -j2 && sudo make install
cd ../..

echo "Building protobuf from source."
wget https://github.com/google/protobuf/archive/v3.2.0.tar.gz
tar -xzf v3.2.0.tar.gz
cd protobuf-3.2.0
./autogen.sh && ./configure && make -j2 && sudo make install
cd ..

echo "Building protobuf-c from source."
wget https://github.com/protobuf-c/protobuf-c/archive/v1.2.1.tar.gz
tar -xzf v1.2.1.tar.gz
cd protobuf-c-1.2.1
./autogen.sh && ./configure --prefix=/usr && make -j2 && sudo make install
cd ..

git clone -b master https://github.com/sysrepo/sysrepo.git
cd sysrepo; mkdir build; cd build
cmake .. && make -j2 && sudo make install
cd ../..

git clone https://github.com/CESNET/Netopeer2.git
cd Netopeer2
cd keystored && mkdir build && cd build
cmake .. && make -j2 && sudo make install
cd ../..
cd server && mkdir build && cd build
cmake .. && make -j2 && sudo make install
cd ../..
cd cli && mkdir build && cd build
cmake .. && make -j2 && sudo make install
cd ../..
