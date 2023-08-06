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
from time import time
from random import randint
from . import Frame
from . import INT, IP, ADDR







# === ICMP Header === #
class Header(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = INT( 0, size=1 )
        self.code = INT( 0, size=1 )

        self.structure = [
            "type",     # Type
            "code",     # Code
            "checksum"  # Checksum
        ]

        self.checksumstruct = [
            "type",
            "code",
            "payload"
        ]


    @property
    def protocol(self):
        return self.type







# === Echo === #
class Echo(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.id = INT( randint(0, 0xffff), size=2 )
        self.seq = INT( 0, size=2 )
        self.timestamp = INT( int(time()), size=8, format="little" )

        self.structure = [
            "id",               # Identifier
            "seq",              # Sequence number
            "timestamp"         # Timestamp

        ]







# === Time Exceeded === #
class TimeExceeded(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.padding = INT( 0, size=4 )

        self.structure = [
            "padding"           # Padding
        ]







# === Redirect === #
class Redirect(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.type = INT( 5, size=1 )
        self.gateway = IP( "255.255.255.255" )

        self.structure = [
            "gateway"           # Gateway
        ]
