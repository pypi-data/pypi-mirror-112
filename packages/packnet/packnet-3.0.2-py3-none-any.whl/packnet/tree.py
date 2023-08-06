"""

 PACKNET  -  c0mplh4cks

 TREE


"""





# === Importing Dependencies === #
from . import ETHERNET
from . import ARP, IPv4, IPv6
from . import UDP, TCP, ICMP, ICMPv6
from . import DNS







# === Tree === #
class Tree:
    @classmethod
    def get(cls, parent=None, child=None, edge=None):
        for node in cls.nodes:
            p, c, e = node
            result = [p==parent, c==child, e==edge]
            if result.count(True) == 2:
                return node[ result.index(False) ]


    @classmethod
    def getnodes(cls, parent=None, child=None, edge=None):
        out = []

        for node in cls.nodes:
            p, c, e = node
            result = [p==parent, c==child, e==edge]

            if True in result:
                out.append(node)

        return out







# === Protocol Tree === #
class Protocoltree(Tree):
    nodes = [
        [ ETHERNET.Header, IPv4.Header, 0x0800 ],
        [ ETHERNET.Header, ARP.Header, 0x0806 ],

        [ IPv4.Header, ICMP.Header, 1 ],
        [ IPv4.Header, UDP.Header, 17 ],
        [ IPv4.Header, TCP.Header, 6 ],

        [ UDP.Header, DNS.Header, 53 ],
        #[ UDP.Header, DHCP.Header, 67 ],
        #[ UDP.Header, DHCP.Header, 68 ],

        [ ICMP.Header, ICMP.Echo, 8 ],
        [ ICMP.Header, ICMP.Echo, 0 ],
        [ ICMP.Header, ICMP.TimeExceeded, 11 ],
        [ ICMP.Header, ICMP.Redirect, 5 ],

        [ ICMPv6.Header, ICMPv6.Echo, 128 ],
        [ IPv6.Header, ICMPv6.Header, 58 ],
    ]
