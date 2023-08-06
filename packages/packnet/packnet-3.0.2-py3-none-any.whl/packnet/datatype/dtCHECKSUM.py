"""

 PACKNET  -  c0mplh4cks

 DATATYPE
    CHECKSUM



"""





# === Importing Dependencies === #
from struct import pack, unpack
from . import INT







# === CHECKSUM === #
class CHECKSUM(INT):
    def __init__(self, *args):
        super().__init__()

        self.size = 2
        self.checksum = args


    @property
    def checksum(self):
        return self.integer


    @checksum.setter
    def checksum(self, data):
        if type(data) == bytes:
            value = data
        else:
            data = b"".join([ v.to_bytes() if type(v) != bytes else v for v in data ])
            value = self.calculate(data)
        self.integer = value



    @staticmethod
    def calculate(data):
        if (len(data) %2) != 0:
            data += b"\x00"

        values = unpack( f">{len(data)//2}H", data )
        n = sum(values) %65535
        n = 65535-n

        return n
