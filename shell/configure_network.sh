#!/bin/sh

# Copy iptables and route-eth1
cp /vagrant/shell/iptables /etc/sysconfig
cp /vagrant/shell/route-eth1 /etc/sysconfig/network-scripts

service iptables restart
service network restart
