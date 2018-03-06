#!/bin/bash

apt-get install zlib1g-dev libssl-dev libavl-dev libev-dev coreutils acl valgrind autoconf libtool
apt-get install gcc make cmake doxygen swig python-dev lua5.2 git build-essential devscripts debhelper
apt-get install bison flex libpcre3-dev 
# libprotobuf-c-dev protobuf-c-compiler

echo "Building cmocka library from source"
if [ ! -d "cmocka/build" ]; then
	wget https://cmocka.org/files/1.0/cmocka-1.0.1.tar.xz
	tar -xJvf cmocka-1.0.1.tar.xz
	mv cmocka-1.0.1 cmocka
	cd cmocka && mkdir build && cd build
	cmake .. && make -j8 && make install
	cd ../..
	rm cmocka-1.0.1.tar.xz
else
	cd cmocka/build
    make install
    cd ../..
fi

echo "Building libyang library from source"
git clone https://github.com/CESNET/libyang.git
cd libyang; mkdir build; cd build
cmake .. && make -j8 && make install
cd ../..

echo "Building libssh library from source"
if [ ! -d "libssh-/build" ]; then
	wget https://git.libssh.org/projects/libssh.git/snapshot/libssh-0.7.5.tar.gz
	tar -xzf libssh-0.7.5.tar.gz
	mv libssh-0.7.5 libssh
	cd libssh; mkdir build; cd build
	cmake .. && make -j8 && make install	
	cd ../..
	rm libssh-0.7.5.tar.gz
else
	cd libssh/build
    make install
    cd ../..
fi

echo "Building libnetconf2 library from source"
git clone https://github.com/CESNET/libnetconf2.git
cd libnetconf2; mkdir build; cd build
cmake .. && make -j8 && make install
cd ../..

echo "Building protobuf library from source"
if [ ! -f "protobuf/Makefile" ]; then
	wget https://github.com/google/protobuf/archive/v3.2.0.tar.gz
	tar -xzf v3.2.0.tar.gz
	mv protobuf-3.2.0 protobuf
	cd protobuf
	./autogen.sh
	./configure
	make -j8 && make install
	cd ..
	rm v3.2.0.tar.gz
else
    cd protobuf
    make install
    cd ..
fi

echo "Building sysrepo library from source"
git clone https://github.com/sysrepo/sysrepo.git
cd sysrepo; mkdir build; cd build
cmake .. && make -j8 && make install
cd ../..

# BUG sysrepo
cp /root/YANG/ietf-keystore@2016-10-31.yang /root/sysrepo/build/repository/yang/ &&
cp /root/YANG/ietf-netconf-server@2016-11-02.yang /root/sysrepo/build/repository/yang/ &&
cp /root/YANG/ietf-x509-cert-to-name@2014-12-10.yang /root/sysrepo/build/repository/yang/ &&
cp /root/YANG/ietf-ssh-server@2016-11-02.yang /root/sysrepo/build/repository/yang/ &&
cp /root/YANG/ietf-tls-server@2016-11-02.yang /root/sysrepo/build/repository/yang/ &&
cp /root/YANG/ietf-system@2014-08-06.yang /root/sysrepo/build/repository/yang/ &&
cp /root/YANG/iana-crypt-hash@2014-08-06.yang /root/sysrepo/build/repository/yang/ &&
cp ietf-keystore.persist /root/sysrepo/build/repository/data/ &&
cp ietf-keystore.running /root/sysrepo/build/repository/data/ &&
cp ietf-keystore.running.lock /root/sysrepo/build/repository/data/ &&
cp ietf-keystore.startup /root/sysrepo/build/repository/data/ &&
cp ietf-keystore.startup.lock /root/sysrepo/build/repository/data/ 

sysrepoctl --install --yang=/root/sysrepo/build/repository/yang/ietf-keystore@2016-10-31.yang --owner=root:root --permissions=666 &&
sysrepoctl --install --yang=/root/sysrepo/build/repository/yang/ietf-netconf-server@2016-11-02.yang --owner=root:root --permissions=666
#

sysrepoctl --install --yang=/root/sysrepo/build/repository/yang/test.yang --owner=root:root --permissions=644 &&
sysrepoctl --install --yang=/root/sysrepo/build/repository/yang/bluespace_node.yang --owner=root:root --permissions=644 &&
sysrepoctl --install --yang=/root/sysrepo/build/repository/yang/sdm_node.yang --owner=root:root --permissions=644
#

echo "Building Netopeer2 from source"
git clone https://github.com/CESNET/Netopeer2.git
cd Netopeer2

echo "Building keystored"
cd keystored && mkdir build && cd build
cmake .. && make && make install 
cd ../..

echo "Building server"
cd server && mkdir build && cd build
cmake .. && make && make install 
cd ../..

echo "Building client"
cd cli && mkdir build && cd build
cmake ..
make -j8 && make install && cd
