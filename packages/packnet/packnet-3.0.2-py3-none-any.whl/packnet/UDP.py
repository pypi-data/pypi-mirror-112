"""

 PACKNET  -  c0mplh4cks

 UDP

     .---.--------------.
     | 5 | Application  |
     #===#==============#
     # 4 # Transport    #
     #===#==============#
     | 3 | Network      |
     |---|--------------|
     | 2 | Data Link    |
     |---|--------------|
     | 1 | Physical     |
     '---'--------------'


"""





# === Importing Dependencies === #
from . import Frame
from . import INT, ADDR, CHECKSUM







# === UDP Header === #
class Header(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.src = ADDR()
        self.dst = ADDR()

        self.structure = [
            "src.port",     # Source port
            "dst.port",     # Target port
            "len.total",    # Total length
            "checksum"      # Checksum
        ]

        self.checksumstruct = [
            "src.port",
            "dst.port",
            "len.total",
            "payload",
            "src.ip",
            "dst.ip",
            "len.total",
            b"\x00\x11"
        ]



    @property
    def protocol(self):
        return [ self.src.port.integer, self.dst.port.integer ]
