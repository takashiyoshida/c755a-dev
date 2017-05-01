#!/bin/sh

ORACLE_HOME="/u01/app/oracle/product/11.2.0/dbhome_1"
ORACLE_ADMIN="${ORACLE_HOME}/network/admin"
# Copy tnsnames.ora
cp /vagrant/shell/tnsnames.ora /etc/tnsnames.ora
cp /vagrant/shell/tnsnames.ora ${ORACLE_ADMIN}/tnsnames.ora
# Copy listener.ora
cp /vagrant/shell/listener.ora ${ORACLE_ADMIN}/listener.ora

chmod 777 /etc/tnsnames.ora
chmod 644 ${ORACLE_ADMIN}/tnsnames.ora
chmod 644 ${ORACLE_ADMIN}/listener.ora
