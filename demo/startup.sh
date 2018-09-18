#!/bin/bash

#vlan
vconfig add enp0s3 10
vconfig add enp0s3 11
vconfig add enp0s3 12
vconfig add enp0s3 13
vconfig add enp0s3 14
vconfig add enp0s3 15
vconfig add enp0s3 16

#ovs
ovs-ctl --system-id=random start

#screen
screen -Sdm ryu
screen -Sdm pced
screen -Sdm pcedML
screen -Sdm pceL2
screen -Sdm provisioning
screen -Sdm abno
