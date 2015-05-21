#!/usr/bin/env python

from __future__ import print_function
import socket
import struct
import sys

ADDRESS='224.1.1.1'
PORT=2240
TTL=1

def error(msg, arg):
    print(msg, arg, file=sys.stderr)
    print('Usage:', sys.argv[0], '[--listen] [address [port [TTL]]]',
          file=sys.stderr)
    sys.exit(1)

if len(sys.argv) > 2:
    try:
        PORT = int(sys.argv[2])
        if PORT < 1025 and PORT > 65534 : raise ValueError()
    except:
        error('Error: unrecognized port number', sys.argv[2])

if len(sys.argv) > 3:
    try:
        TTL = int(sys.argv[3])
        if TTL < 1 and TTL > 128 : raise ValueError()
    except:
        error('Error: unrecognized TTL number', sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except:
    error('Error: fail installing listening', 'socket')

try:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
except:
    pass # Some systems don't support SO_REUSEPORT


try:
    sock.bind(('', PORT))
except:
    error('Error: bind error for host', ADDRESS)

mreq = struct.pack('=4sl', socket.inet_aton(ADDRESS), socket.INADDR_ANY)
try:
    socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
except:
    error('Error: refuse to add membership to', ADDRESS)

try:
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, TTL)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
except:
    try:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
    except:
        pass
    error('Error: refuse to set TTL and LOOP on', 'socket')

try:
    sock.setblocking(0)
except:
    try:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
    except:
        pass
    error('Error: refuse to set non-blocking', 'socket')

print('Joined group', ADDRESS, 'on port', PORT, 'sending with TTL of', TTL)
import time

rcnt = 0
scnt = 0

try:
    while True:
        reply = None
        try:
            reply = sock.recv(5)
        except socket.error:
            time.sleep(0.5)
            sock.sendto(b'mping', (ADDRESS, PORT))
            print('Ping sent')
            scnt += 1
            continue
        if reply != None:
            print('Ping received')
            if reply != b'mping':
                print('Warning: unexpected payload')
            rcnt += 1
except:
    try:
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_DROP_MEMBERSHIP, mreq)
    except:
        pass

    print()
    print('Received', rcnt, 'packets and sent', scnt, 'packets')
    sys.exit(0)
