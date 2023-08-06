"""

 PACKNET  -  c0mplh4cks

 TCP

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
from . import INT, ADDR, LEN





# === TCP Header === #
class Header(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.src = ADDR()
        self.dst = ADDR()
        self.version = INT( 6, size=2 )
        self.seq = INT( 0, size=4 )
        self.ack = INT( 0, size=4 )
        self.flags = INT( 0 )
        self.win = INT( 65000, size=2)
        self.urg = INT( 0, size=2 )

        self.options = []
        self.optiontree = { opt().code.integer : opt for opt in [Padding, MSS, Window, SACKpermit, Timestamp] }

        self.structure = [
            "src.port", # Source port
            "dst.port", # Target port
            "seq",      # Sequence number
            "ack",      # Acknowledgement number
            "hlf",      # Header length & Flags
            "win",      # Window size
            "urg",      # Urgent pointer
            "checksum"  # Checksum
        ]

        self.checksumstruct = [
            "src.port",
            "dst.port",
            "seq",
            "ack",
            "hlf",
            "win",
            "urg",
            "src.ip",
            "dst.ip",
            "version",
            "len.total"
        ]



    @property
    def protocol(self):
        return [ self.src.port.integer, self.dst.port.integer ]


    @property
    def hlf(self):
        i = (self.len.header.integer // 4 << 12) + self.flags.integer
        return INT( i, size=2 )


    @hlf.setter
    def hlf(self, value):
        i = value.integer
        self.len.header.integer = (i >> 12) * 4
        self.flags.integer = i - (self.len.header.integer // 4 << 12)



    def rlen(self):
        super().rlen()
        self.len.header.integer += sum([ len(option) for option in self.options])


    def pad(self):
        pass    # autopadding


    def to_bytes(self, *args, **kwargs):
        packet = super().to_bytes(*args, **kwargs)

        for option in self.options:
            packet += option.to_bytes()

        return packet


    def from_bytes(self, packet=b"", *args, **kwargs):
        i = super().from_bytes(packet, *args, **kwargs)[0]

        while (i < self.len.header.integer):
            option = self.optiontree[ packet[i] ]()
            i += option.from_bytes( packet[i:], payload=False )[0]
            self.options.append( option )

        self.payload = packet[i:]
        self.rlen()

        return (i,)







# === Padding === #
class Padding(Frame):
    def __init__(self):
        super().__init__()
        self.code = INT( 1, size=1 )
        self.structure = [ "code" ]



# === Maximum Segment Size === #
class MSS(Frame):
    def __init__(self):
        super().__init__()
        self.code = INT( 2, size=1 )
        self.len.size = 1
        self.value = INT( 536, size=2 )
        self.structure = [ "code", "len.header", "value" ]



# === Window Scale === #
class Window(Frame):
    def __init__(self):
        super().__init__()
        self.code = INT( 3, size=1 )
        self.len.size = 1
        self.value = INT( 0, size=1 )
        self.structure = [ "code", "len.header", "value" ]



# === Selective ACKnowledgement Permitted === #
class SACKpermit(Frame):
    def __init__(self):
        super().__init__()
        self.code = INT( 4, size=1 )
        self.len.size = 1
        self.structure = [ "code", "len.header" ]



# === Timestamp === #
class Timestamp(Frame):
    def __init__(self):
        super().__init__()
        self.code = INT( 8, size=1 )
        self.len.size = 1
        self.left = INT( 0, size=4 )
        self.right = INT( 0, size=4 )
        self.structure = [ "code", "len.header", "left", "right" ]
