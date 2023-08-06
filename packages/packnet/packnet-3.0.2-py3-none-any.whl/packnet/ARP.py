"""

 PACKNET  -  c0mplh4cks

 ARP

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







# === ARP Header === #
class Header(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.src = ADDR( ip="255.255.255.255", mac="ff:ff:ff:ff:ff:ff" )
        self.dst = ADDR( ip="255.255.255.255", mac="ff:ff:ff:ff:ff:ff" )
        self.op = INT( 1, size=2 )
        self.ht = INT( 1, size=2 )
        self.pt = INT( 0x0800, size=2 )
        self.hs = INT( 6, size=1 )
        self.ps = INT( 4, size=1 )
        self.protocol = None

        self.structure = [
            "ht",       # Hardware type
            "pt",       # Protocol type
            "hs",       # Hardware size
            "ps",       # Protocol size
            "op",       # Operation code
            "src.mac",  # Source MAC
            "src.ip",   # Source IP
            "dst.mac",  # Target MAC
            "dst.ip"    # Target IP
        ]
