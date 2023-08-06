"""

 PACKNET  -  c0mplh4cks

 PACKAGER


"""





# === Importing Dependencies === #
from . import Frame
from . import Protocoltree
from . import ETHERNET
from . import ADDR







# === Packager === #
class Packager(Frame):
    def __init__(self, startprotocol=ETHERNET.Header, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.startprotocol = startprotocol

        self.__src = ADDR()
        self.__dst = ADDR()

        for i in range(4):
            setattr(self, f"l{i}", b"")

        self.structure = [
            f"l{i}" for i in range(4)
        ]


    def __getitem__(self, key):
        if (-1 >= key > -5):
            key = 4+key
        if (0 <= key < 4):
            return getattr(self, f"l{key}")
        raise IndexError


    def __setitem__(self, key, value):
        if (-1 >= key > -5):
            key = 4-key
        if (0 <= key < 4):
            return setattr(self, f"l{key}", value)
        raise IndexError



    @property
    def src(self):
        if self[0]: self.__src.mac = self[0].src.mac
        if self[1]: self.__src.ip = self[1].src.ip
        if self[2]: self.__src.port = self[2].src.port
        return self.__src


    @src.setter
    def src(self, value):
        self.__src.addr = value
        for protocol in self:
            if type(protocol) != bytes:
                if hasattr(protocol, "src"):
                    protocol.src.addr = self.__src.addr


    @property
    def dst(self):
        if self[0]: self.__dst.mac = self[0].dst.mac
        if self[1]: self.__dst.ip = self[1].dst.ip
        if self[2]: self.__dst.port = self[2].dst.port
        return self.__dst


    @dst.setter
    def dst(self, value):
        self.__dst.addr = value
        for protocol in self:
            if type(protocol) != bytes:
                if hasattr(protocol, "dst"):
                    protocol.dst.addr = self.__dst.addr



    def fill(self, protocol):
        protocols = [ protocol ]

        while True:
            node = Protocoltree.getnodes( child=protocol )
            if not node: break
            protocol = node[0][0]
            protocols.insert( 0, protocol )

        for i, protocol in enumerate(protocols):
            self[i] = protocol()

        for i, protocol in enumerate(protocols[:-1]):
            edge = Protocoltree.get( parent=type(self[i]), child=type(self[i+1]) )
            if type(self[i].protocol) != list:
                self[i].protocol.integer = edge


    def to_bytes(self, *args, **kwargs):
        packet = b""

        for i in range(1, 4)[::-1]:
            if type( self[i] ) != bytes:
                self[i-1].payload = self[i].packet

        return (self[0].packet + self.payload)


    def from_bytes(self, packet=b"", *args, **kwargs):
        protocol = self.startprotocol
        i = 0

        for l in range(4):
            self[l] = protocol()
            i += self[l].from_bytes( packet[i:] )[0]
            next = self[l].protocol
            if next == None: break
            next = next if type(next) == list else [int(next)]
            for edge in next:
                protocol = Protocoltree.get( parent=protocol, edge=edge )
                if protocol: break
            if protocol == None: break

        self.src = self.src
        self.dst = self.dst

        return (i,)
