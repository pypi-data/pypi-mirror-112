"""

 PACKNET  -  c0mplh4cks

 FRAME


"""





# === Importing Dependencies === #
from . import LEN, CHECKSUM, NAME







# === Frame === #
class Frame:
    def __init__(self):
        self.payload = b""
        self.len = LEN()
        self.structure = []
        self.ERROR = None


    def __len__(self):
        self.rlen()
        return self.len.total.integer



    @property
    def packet(self):
        return self.to_bytes() + self.payload


    @packet.setter
    def packet(self, encoded):
        self.from_bytes(encoded)


    @property
    def checksum(self):
        return CHECKSUM(
            *[ self._getattr(attr) if type(attr) != bytes else attr for attr in self.checksumstruct ]
        )


    @checksum.setter
    def checksum(self, value):
        if int(value) != int(self.checksum):
            self.ERROR = "incorrect checksum"



    def _getattr(self, attrstr):
        attr = self

        for part in attrstr.split("."):
            attr = getattr(attr, part)

        return attr


    def _setattr(self, attrstr, value):
        if "." in attrstr:
            o, attr = attrstr.rsplit(".", 1)
            o = self._getattr(o)
        else:
            o, attr = self, attrstr
        setattr(o, attr, value)



    def rlen(self):
        self.len.header.integer = sum([ len(self._getattr(attr)) for attr in self.structure ])
        self.len.payload.integer = len(self.payload)


    def to_bytes(self, header=False, *args, **kwargs):
        self.rlen()
        packet = []

        for attrstr in self.structure:
            attr = self._getattr(attrstr)

            if type(attr) == bytes:
                packet.append( attr )
            else:
                parenthdr = header + b"".join(packet) if header else b""
                packet.append( attr.to_bytes( header=parenthdr ) )

        return b"".join(packet)


    def from_bytes(self, packet=b"", header=False, payload=True):
        i = 0
        tasks = {}

        for attrstr in self.structure:
            attr = self._getattr(attrstr)
            if type(attr) != bytes:
                parenthdr = header + packet[:i] if header else b""
                i += attr.from_bytes( packet[i:], header=parenthdr )[0]
                tasks[attrstr] = attr

        if payload:
            self.payload = packet[i:]
        self.rlen()
        for attrstr, attr in tasks.items():
            self._setattr(attrstr, attr)

        return (i,)


    def debug(self):
        print( "# === START DEBUG INFO === #" )
        print( self )

        print( f"\n{'ATTRIBUTE NAME':<20}VALUE\n")
        print( f"{'len':<20}{self.len}")
        for attrstr in self.structure:
            print( f"{attrstr:<20}{self._getattr(attrstr)}" )
        print( f"{'payload':<20}{self.payload}")
        print( "\n# === END DEBUG INFO === #" )
