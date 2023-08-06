"""

 PACKNET  -  c0mplh4cks

 IPV4

     .---.--------------.
     | 5 | Application  |
     |---|--------------|
     | 4 | Transport    |
     #===#==============#
     # 3 # Network      #
     #===#==============#
     | 2 | Data Link    |
     |---|--------------|
     | 1 | Physical     |
     '---'--------------'


"""





# === Importing Dependencies === #
from random import randint
from . import Frame
from . import INT, ADDR







# === IPv4 Header === #
class Header(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.src = ADDR( ip="255.255.255.255" )
        self.dst = ADDR( ip="255.255.255.255" )
        self.version = INT( 4 )
        self.protocol = INT( 17, size=1 )
        self.id = INT( randint(0, 0xffff), size=2 )
        self.dscp = INT( 0 , size=1 )
        self.flags = INT( 0b010 << 13, size=2 )
        self.ttl = INT( 64, size=1 )

        self.structure = [
            "vhl",
            "dscp",
            "len.total",
            "id",
            "flags",
            "ttl",
            "protocol",
            "checksum",
            "src.ip",
            "dst.ip"
        ]

        self.checksumstruct = [
            "vhl",
            "dscp",
            "len.total",
            "id",
            "flags",
            "ttl",
            "protocol",
            "src.ip",
            "dst.ip"
        ]



    @property
    def vhl(self):
        i = (self.version.integer << 4) + (self.len.header.integer // 4)
        return INT( i, size=1 )


    @vhl.setter
    def vhl(self, value):
        i = value.integer
        self.version.integer = i >> 4
        self.len.header.integer = (i - (self.version.integer << 4)) * 4
