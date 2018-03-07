#!/bin/bash

apt-get install zlib1g-dev libssl-dev libavl-dev libev-dev coreutils acl valgrind autoconf libtool
apt-get install gcc make cmake doxygen swig python-dev lua5.2 git build-essential devscripts debhelper
apt-get install bison flex libpcre3-dev libprotobuf-c-dev protobuf-c-compiler

echo "Building cmocka library from source"
if [ ! -d "cmocka/build" ]; then
	wget https://cmocka.org/files/1.0/cmocka-1.0.1.tar.xz
	tar -xJvf cmocka-1.0.1.tar.xz
	cd cmocka-1.0.1 && mkdir build && cd build
	cmake .. && make -j8 && sudo make install
	cd ../..
	rm cmocka-1.0.1.tar.xz
else
    cd cmocka-1.0.1/build
    sudo make install
    cd ../..
fi

echo "Building libyang library from source"
git clone https://github.com/CESNET/libyang.git
cd libyang; mkdir build; cd build
cmake .. && make -j8 && sudo make install
cd ../..

echo "Building libssh library from source"
if [ ! -d "libssh-/build" ]; then
	wget https://git.libssh.org/projects/libssh.git/snapshot/libssh-0.7.5.tar.gz
	tar -xzf libssh-0.7.5.tar.gz
	cd libssh-0.7.5; mkdir build; cd build
	cmake .. && make -j8 && sudo make install	
	cd ../..
	rm libssh-0.7.5.tar.gz
else
    cd ibssh-0.7.5/build
    sudo make install
    cd ../..
fi

echo "Building libnetconf2 library from source"
git clone https://github.com/CESNET/libnetconf2.git
cd libnetconf2; mkdir build; cd build
cmake .. && make -j8 && sudo make install
cd ../..

echo "Building protobuf library from source"
if [ ! -f "protobuf/Makefile" ]; then
	wget https://github.com/google/protobuf/archive/v3.2.0.tar.gz
	tar -xzf v3.2.0.tar.gz
	cd protobuf-3.2.0
	./autogen.sh
	./configure
	make -j8 && make sudo install
	cd ..
	rm v3.2.0.tar.gz
else
    cd protobuf-3.2.0
    sudo make install
    cd ..
fi

echo "Building sysrepo library from source"
git clone https://github.com/sysrepo/sysrepo.git
cd sysrepo; mkdir build; cd build
cmake .. && make -j8 && sudo make install
ldconfig
cd ../..

echo "Building Netopeer2 from source"
git clone https://github.com/CESNET/Netopeer2.git
cd Netopeer2

echo "Building keystored"
cd keystored && mkdir build && cd build
cmake .. && make && sudo make install 
cd ../..

echo "Building server"
cd server && mkdir build && cd build
cmake .. && make && sudo make install 
cd ../..

echo "Building client"
cd cli && mkdir build && cd build
cmake ..
make -j8 && sudo make install && cd
