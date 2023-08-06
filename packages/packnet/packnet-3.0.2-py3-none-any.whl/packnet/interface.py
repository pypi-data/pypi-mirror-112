"""

 PACKNET  -  c0mplh4cks

 INTERFACE


"""





# === Importing Dependencies === #
import socket
from time import time
from .standards import encode, decode
from . import ADDR, MAC







# === Interface === #
class Interface():
    def __init__(self, card=None, port=0, passive=False, timeout=64):
        self.passive = passive

        self.sock = socket.socket( socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003) )
        self.sock.settimeout(timeout)

        if not card:
            self.card = [ i[1] for i in socket.if_nameindex() ][-1]
        else:
            self.card = card

        if not passive:
            s = socket.socket( socket.AF_INET, socket.SOCK_DGRAM )
            s.setsockopt( socket.SOL_SOCKET, 25, f"{self.card}".encode() )
            s.connect( ("1.1.1.1", 80) )
            ip = s.getsockname()[0]

            self.sock.bind( (self.card, 0) )
            mac = MAC.decode( self.sock.getsockname()[4] )[1]

            self.addr = ADDR(ip, port, mac)



    def send(self, packet):
        self.sock.send(packet)


    def recv(self, length=2048):
        return self.sock.recvfrom(length)
