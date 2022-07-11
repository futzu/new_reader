"""
new_reader.py
Home of the reader function
"""

import socket
import struct
import sys
import urllib.request


MAJOR = "0"
MINOR = "0"
MAINTAINENCE = "9"


def version():
    """
    version prints version as a string

    Odd number versions are releases.
    Even number versions are testing builds between releases.

    Used to set version in setup.py
    and as an easy way to check which
    version you have installed.

    """
    return f"{MAJOR}.{MINOR}.{MAINTAINENCE}"


def version_number():
    """
    version_number returns version as an int.
    if version() returns 2.3.01
    version_number will return 2301
    """
    return int(f"{MAJOR}{MINOR}{MAINTAINENCE}")


def reader(uri):
    """
    reader returns an open file handle.
    stdin:              cat video.ts | gumd
    files:              "/home/you/video.ts"
    http(s) urls:       "https://example.com/vid.ts"
    udp urls:           "udp://1.2.3.4:5555"
    multicast urls:     "udp://@227.1.3.10:4310"



    Use like:

    with reader("udp://@227.1.3.10:4310") as data:
        data.read(8192)

    with reader("/home/you/video.ts") as data:
        fu = data.read()

    udp_data =reader("udp://1.2.3.4:5555")
    chunks = [udp_data.read(188) for i in range(0,1024)]
    udp_data.close()



    """
    # read from stdin
    if uri in [None, sys.stdin.buffer]:
        return sys.stdin.buffer
    # Multicast
    if uri.startswith("udp://@"):
        return _open_mcast(uri)
    # Udp
    if uri.startswith("udp://"):
        return _open_udp(uri)
    # Http(s)
    if uri.startswith("http"):
        return urllib.request.urlopen(uri)
    # File
    return open(uri, "rb")


def _read_stream(sock):
    """
    return a socket that can be read like a file.
    """
    return sock.makefile(mode="rb")


def _udp_sock_opts(sock):
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 90000000)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # return sock


def _mk_udp_sock(udp_ip, udp_port):
    """
    udp socket setup
    """
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    _udp_sock_opts(sock)
    sock.bind((udp_ip, udp_port))
    return sock


def _mk_mcast_sock(mcast_grp, mcast_port, all_grps=True):
    """
    multicast socket setup
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    _udp_sock_opts(sock)
    if all_grps:
        sock.bind(("", mcast_port))
    else:
        sock.bind((mcast_grp, mcast_port))
    mreq = struct.pack("4sl", socket.inet_aton(mcast_grp), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    return sock


def _open_udp(uri):
    """
    udp://1.2.3.4:5555
    """
    udp_ip, udp_port = (uri.split("udp://")[1]).rsplit(":",1)
    udp_port = int(udp_port)
    udp_sock = _mk_udp_sock(udp_ip, udp_port)
    return _read_stream(udp_sock)


def _open_mcast(uri):
    """
    udp://@227.1.3.10:4310
    """
    mcast_grp, mcast_port = (uri.split("udp://@")[1]).rsplit(":",1)
    mcast_port = int(mcast_port)
    mcast_sock = _mk_mcast_sock(mcast_grp, mcast_port)
    return _read_stream(mcast_sock)
