"""
new_reader.py
Home of the reader function
"""

import socket
import struct
import sys
import urllib.request


MAJOR = "0"
MINOR = "1"
MAINTAINENCE = "05"


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


def reader(uri, headers={}):
    """
    reader returns an open file handle.
    stdin:              cat video.ts | gumd
    files:              "/home/you/video.ts"
    http(s) urls:       "https://example.com/vid.ts"
     (http headers can be added by setting headers)
    udp urls:           "udp://1.2.3.4:5555"
    multicast urls:     "udp://@227.1.3.10:4310"

    Use like:

    with reader('http://iodisco.com/') as disco:
        disco.read()

    with reader('http://iodisco.com/',headers={"myHeader":"DOOM"}) as doom:
        doom.read()

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
        req = urllib.request.Request(uri,headers=headers)
        return urllib.requesturlopen(req)
    # File
    return open(uri, "rb")


def _read_stream(sock):
    """
    return a socket that can be read like a file.
    """
    return sock.makefile(mode="rb")


def double_rcvbuf(sock):
    """
    double_rcvbuf doubles socket.SO_RCVBUF
    until it errors
    """
    rcvbuf_size = sock.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
    while True:
        try:
            rcvbuf_size += rcvbuf_size
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, rcvbuf_size)
        except:
            break


def _mk_sock():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    double_rcvbuf(sock)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    if hasattr(socket, "SO_REUSEPORT"):
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    return sock


def _mk_udp_sock(udp_ip, udp_port):
    """
    udp socket setup
    """
    udp_sock = _mk_sock()
    udp_sock.bind((udp_ip, udp_port))
    return _read_stream(udp_sock)


def _mk_mcast_sock(mcast_grp, mcast_port):
    """
    multicast socket setup
    """
    mcast_host = "0.0.0.0"
    mcast_sock = _mk_sock()
    mcast_sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(mcast_grp) + socket.inet_aton(mcast_host),
    )
    mcast_sock.bind((mcast_host, mcast_port))
    return _read_stream(mcast_sock)


def _open_udp(uri):
    """
    udp://1.2.3.4:5555
    """
    udp_ip, udp_port = (uri.split("udp://")[1]).rsplit(":", 1)
    udp_port = int(udp_port)
    return _mk_udp_sock(udp_ip, udp_port)


def _open_mcast(uri):
    """
    udp://@227.1.3.10:4310
    """
    mcast_grp, mcast_port = (uri.split("udp://@")[1]).rsplit(":", 1)
    mcast_port = int(mcast_port)
    return _mk_mcast_sock(mcast_grp, mcast_port)
