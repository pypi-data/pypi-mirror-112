"""

 PACKNET  -  c0mplh4cks

 ICMP

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





# === ICMP Header === #
class Header(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = INT( 0, size=1 )
        self.code = INT( 0, size=1 )
        self.src = ADDR( version=6 )
        self.dst = ADDR( version=6 )
        self.protocol = None

        self.structure = [
            "type",     # Type
            "code",     # Code
            "checksum"  # Checksum
        ]

        self.checksumstruct = [
            "type",
            "code",
            "payload",
            "src.ip",
            "dst.ip",
            "len.header",
            b"\x3a"
        ]


    @property
    def protoccol(self):
        return self.type







# === Echo === #
class Echo(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = INT( randint(0, 0xffff), size=2 )
        self.seq = INT( 0, size=2 )

        self.structure = [
            "id",               # Identifier
            "seq"               # Sequence number
        ]
