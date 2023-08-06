"""

 PACKNET  -  c0mplh4cks

 GENERAL


"""





# === Importing Dependencies === #
import socket
from .vendor import vendors
from time import time
from . import Packager
from . import ARP
from .interface import Interface







# === Get Public IP === #
def getpublicip():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect( ("ifconfig.me", 80) )
    s.send( b"GET http://ifconfig.me HTTP/1.1\r\n\r\n" )
    data = s.recv(1024).decode()

    return data.split("\r\n\r\n")[1]





# === Mac Vendor Lookup === #
def maclookup(mac):
    mac = mac.upper().replace(":", "")

    vendor = vendors.get( mac[:6] )

    return vendor





# === Get MAC === #
def getmac(ip, interface=None, timeout=3):
    if not interface: interface = Interface()
    if interface.passive: return None

    src = interface.addr.addr
    dst = [ip, 0, "ff:ff:ff:ff:ff:ff"]

    package = Packager()
    package.fill( ARP.Header )
    package.src = src
    package.dst = dst

    interface.sock.settimeout(timeout)
    interface.send( package.packet )

    start = time()
    while ( (time() - start) < timeout ):
        try:
            packet, info = interface.recv()
        except socket.timeout:
            return None

        try:
            package = Packager()
            package.packet = packet
        except:
            continue

        if type( package[1] ) != ARP.Header: continue
        if str(package.dst.mac) != str(interface.addr.mac) != str(package[1].dst.mac): continue
        if str(package[1].src.ip) != ip: continue

        return package[1].src
