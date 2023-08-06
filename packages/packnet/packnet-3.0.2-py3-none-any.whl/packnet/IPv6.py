"""

 PACKNET  -  c0mplh4cks

 IPv6

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
from . import Frame
from . import INT, ADDR






# === IPv6 Header === #
class Header(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.src = ADDR( version=6 )
        self.dst = ADDR( version=6 )
        self.version = INT( 6 )
        self.traffic = INT( 0 )
        self.flowlabel = INT( 0 )
        self.hop = INT( 64, size=1 )
        self.protocol = INT( 58, size=1 )
        self.vtf = INT( 0, size=4 )

        self.structure = [
            "vtf",
            "len.payload",
            "protocol",
            "hop",
            "src.ip",
            "dst.ip"
        ]



    @property
    def vtf(self):
        i = (self.version.integer << 24) + (self.traffic.integer << 20) + (self.flowlabel.integer)
        return INT( i, size=4 )


    @vtf.setter
    def vtf(self, value):
        i = value.integer
        self.version.integer = i >> 24
        self.traffic.integer = (i - (self.version.integer << 24)) >> 20
        self.flowlabel.integer = (i - (self.version.integer << 24) - (self.traffic.integer << 20))
