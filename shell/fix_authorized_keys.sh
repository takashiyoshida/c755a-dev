#!/bin/sh

# For some reasons, vagrant modifies the permission bits of authorized_keys incorrectly.
# This will fix the permission bits and allow the user to log in via SSH.

chmod 600 /home/vagrant/.ssh/authorized_keys
