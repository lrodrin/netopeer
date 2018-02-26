!/bin/bash

apt-get install zlib1g-dev libssl-dev libavl-dev libev-dev coreutils acl valgrind autoconf libtool
apt-get install gcc make cmake doxygen swig python-dev lua5.2 git build-essential devscripts debhelper
apt-get install bison flex libpcre3-dev libprotobuf-c-dev protobuf-c-compiler 

echo "Building cmocka library from source"
wget https://cmocka.org/files/1.0/cmocka-1.0.1.tar.xz
tar -xJvf cmocka-1.0.1.tar.xz
mv cmocka-1.0.1 cmocka
cd cmocka && mkdir build && cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr .. && make -j8 && make install
cd ../..
rm cmocka-1.0.1.tar.xz

echo "Building libyang library from source"
git clone https://github.com/CESNET/libyang.git
cd libyang; mkdir build; cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr ..
make -j8 && make install
cd ../..

echo "Building libssh library from source"
wget https://git.libssh.org/projects/libssh.git/snapshot/libssh-0.7.5.tar.gz
tar -xzf libssh-0.7.5.tar.gz
mv libssh-0.7.5 libssh
cd libssh; mkdir build; cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr .. && make -j8 && make install
cd ../..
rm libssh-0.7.5.tar.gz

echo "Building libnetconf2 library from source"
git clone https://github.com/CESNET/libnetconf2.git
cd libnetconf2; mkdir build; cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr ..
make -j8 && make install
cd ../..

echo "Building protobuf library from source"
git clone https://github.com/google/protobuf.git
cd protobuf
./autogen.sh && ./configure --prefix=/usr && make -j8 && make install
cd ..

echo "Building sysrepo library from source"
git clone https://github.com/sysrepo/sysrepo.git
cd sysrepo; mkdir build; cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=/usr ..
make -j8 && make install
cd ../..

pip install codecov

echo "Building Netopeer2 from source"
git clone https://github.com/CESNET/Netopeer2.git
cd Netopeer2
echo "Building keystored"
cd keystored && mkdir build && cd build
cmake ..
make -j8 && make install 
cd ../..
echo "Building server"
cd server && mkdir build && cd build
cmake ..
make -j8 && make install && 
cd ../..
echo "Building client"
cd cli && mkdir build && cd build
cmake ..
make -j8 && make install && cd

