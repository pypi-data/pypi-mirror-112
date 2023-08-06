"""

 PACKNET  -  c0mplh4cks

 ETHERNET

     .---.--------------.
     | 5 | Application  |
     |---|--------------|
     | 4 | Transport    |
     |---|--------------|
     | 3 | Network      |
     #===#==============#
     # 2 # Data Link    #
     #===#==============#
     | 1 | Physical     |
     '---'--------------'


"""





# === Importing Dependencies === #
from . import Frame
from . import INT, MAC, ADDR







# === Ethernet Header === #
class Header(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.src = ADDR( mac="ff:ff:ff:ff:ff:ff" )
        self.dst = ADDR( mac="ff:ff:ff:ff:ff:ff" )
        self.protocol = INT( 2048, size=2 )

        self.structure = [
                "dst.mac",  # Target MAC
                "src.mac",  # Source MAC
                "protocol"  # Protocol
        ]
